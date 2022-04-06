from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Vehicle
from .raw_queries import VehicleDetailsQuery, GroupsBranchQuery


class BasicVehicleService:

    def __init__(self, vehicle_id: int, session: AsyncSession):
        self.vehicle_id: int = vehicle_id
        self.session: AsyncSession = session

    async def get_vehicle(self) -> Optional[Vehicle]:
        vehicle = await self.session.execute(
            select(Vehicle).where(Vehicle.id == self.vehicle_id)
        )
        vehicle = vehicle.first()
        return vehicle[0] if vehicle else None

    async def _query_group_branch(self, group_id: int) -> Iterable:
        sql_query: str = GroupsBranchQuery.query_string.format(lowest_child=group_id)
        group_branch: Iterable = await self.session.execute(sql_query)
        return group_branch

    async def obtain_vehicle_details(self, vehicle: Vehicle) -> dict:
        functions = {}
        components = {}

        raw_vehicle_details = await self._query_vehicle_details()
        groups_branches = {}

        for row in raw_vehicle_details:
            row_dict: dict = self._unpack_vehicle_details(row)

            if (function_id := row_dict.get("function_id")) is not None:
                if function_id not in functions.keys():
                    function = {
                        "id": function_id,
                        "name": row_dict.get("function_name"),
                        "feature": {
                            "id": row_dict.get("feature_id"),
                            "name": row_dict.get("feature_name")
                        },
                        "components": [],
                        "groups": []
                    }
                    functions[function_id] = function

                if (group_id := row_dict.get("group_id")) not in groups_branches.keys():
                    groups = await self._get_groups_branch(group_id)
                    groups_branches[group_id] = groups

                functions[function_id]["groups"] = groups_branches[group_id]

            if (component_id := row_dict.get("component_id")) is not None:
                if component_id not in components.keys():
                    component = {
                        "id": component_id,
                        "name": row_dict.get("component_name"),
                        "functions": []
                    }
                    components[component_id] = component

                if function_id:
                    components[component_id]["functions"].append(function_id)
                    functions[function_id]["components"].append(component_id)

        vehicle_details = {**vehicle.as_dict}
        vehicle_details["functions"] = functions
        vehicle_details["components"] = components
        return vehicle_details

    async def _query_vehicle_details(self) -> Iterable:
        sql_query: str = VehicleDetailsQuery.query_string.format(vehicle_id=self.vehicle_id)
        vehicle_details: Iterable = await self.session.execute(sql_query)
        return vehicle_details

    def _unpack_vehicle_details(self, row: tuple) -> dict:
        return dict(zip(VehicleDetailsQuery.column_keys, row))

    async def _get_groups_branch(self, group_id: int) -> list[dict]:
        group_branch_rows = await self._query_group_branch(group_id)
        return [dict(zip(GroupsBranchQuery.column_keys, row)) for row in group_branch_rows]
