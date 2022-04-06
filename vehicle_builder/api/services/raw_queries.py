from dataclasses import dataclass


@dataclass
class RawQuery():
    column_keys: tuple
    query_string: str


@dataclass
class VehicleDetailsQuery(RawQuery):
    column_keys = (
        "function_id", "function_name", "feature_id",
        "feature_name", "group_id", "component_id",
        "component_name"
    )
    query_string = """
        SELECT
            func.id as function_id,
            func.name as function_name,
            feat.id as feature_id,
            feat.name as feature_name,
            gr.id as group_id,
            comp.id as component_id,
            comp.name as component_name
        FROM vehicle_features vf
        JOIN "function" func ON func.feature_id = vf.feature_id
        JOIN feature feat ON feat.id = func.feature_id
        JOIN "group" gr ON gr.id = feat.group_id
        LEFT JOIN vehicle_configuration vc ON vc.function_id = func.id
        LEFT JOIN component comp ON comp.id = vc.component_id
        WHERE vf.vehicle_id = {vehicle_id};
    """


@dataclass
class GroupsBranchQuery(RawQuery):
    column_keys = ("group_id", "group_name", "is_set")
    query_string = """
        WITH RECURSIVE rec_anchor AS (
            SELECT
                {lowest_child} AS group_id,
                0 AS n
            UNION ALL
            SELECT
                gr.parent_id,
                rec_anchor.n + 1
            FROM "group" gr
            INNER JOIN rec_anchor ON rec_anchor.group_id = gr.id
        )
        SELECT
            rec_anchor.group_id,
            grp.name,
            grp.is_set
        FROM rec_anchor
        JOIN "group" grp ON grp.id = rec_anchor.group_id
        ORDER BY n;
    """
