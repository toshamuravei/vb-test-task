from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, UniqueConstraint, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base import Base


VEHICLE_WEIGHT_PRECISION: int = 5
VEHICLE_PRICE_PRECISION: int = 3


class Function(Base):
    name = Column(String, nullable=False, unique=True)
    feature_id = Column(Integer, ForeignKey('feature.id', ondelete='CASCADE'))

    feature = relationship("Feature", backref="functions")


class Feature(Base):
    name = Column(String, nullable=False, unique=True)
    group_id = Column(Integer, ForeignKey('group.id', ondelete='CASCADE'))

    group = relationship("Group", backref="features")


class Group(Base):
    name = Column(String, nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey('group.id', ondelete='CASCADE'), nullable=True)
    is_set = Column(Boolean, default=False)


class Component(Base):
    name = Column(String, nullable=False, unique=True)
    cad_model_link = Column(String)
    vendor_code = Column(String)
    supplier_name = Column(String)
    weight = Column(Float(VEHICLE_WEIGHT_PRECISION), default=0)
    price = Column(Float(VEHICLE_PRICE_PRECISION), default=0)
    extra_params = Column(JSONB, default={})


class Vehicle(Base):
    name = Column(String, nullable=False, unique=True)
    extra_params = Column(JSONB, default={})

    @property
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "extra_params": dict(**self.extra_params) if self.extra_params else {}
        }


class VehicleFeatures(Base):
    vehicle_id = Column(Integer, ForeignKey('vehicle.id', ondelete='CASCADE'))
    feature_id = Column(Integer, ForeignKey('feature.id', ondelete='CASCADE'))

    __table_args__ = (UniqueConstraint(vehicle_id, feature_id),)

    vehicle = relationship("Vehicle", backref="vehicle_features")
    feature = relationship("Feature", backref="vehicle_features")


class VehicleConfiguration(Base):
    vehicle_id = Column(Integer, ForeignKey('vehicle.id', ondelete='CASCADE'))
    component_id = Column(Integer, ForeignKey('component.id', ondelete='CASCADE'))
    function_id = Column(Integer, ForeignKey('function.id', ondelete='CASCADE'))

    __table_args__ = (UniqueConstraint(vehicle_id, function_id, component_id),)

    vehicle = relationship("Vehicle", backref="component_configuration")
    function = relationship("Function", backref="vehicle_configuration")
    component = relationship("Component", backref="vehicle_configuration")
