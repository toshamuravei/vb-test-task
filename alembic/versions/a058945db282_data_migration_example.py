"""Data migration: example

Revision ID: a058945db282
Revises: b30351627035
Create Date: 2022-04-04 18:28:22.012765

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'a058945db282'
down_revision = 'b30351627035'
branch_labels = None
depends_on = None


_INSERTS = {
    "function": """
        INSERT INTO
            function (id,name,feature_id)
        VALUES
            (1, 'function #1', 1),
            (2, 'function #2', 1),
            (3, 'function #3', 2),
            (4, 'function #4', 2),
            (5, 'function #5', 3),
            (6, 'function #6', 3);
    """,
    "feature": """
        INSERT INTO
            feature (id,name,group_id)
        VALUES
            (1, 'feature #1', 2),
            (2, 'feature #2', 3),
            (3, 'feature #3', 4);
    """,
    "group": """
        INSERT INTO
            "group" (id,name,parent_id,is_set)
        VALUES
            (1, 'root_group', NULL, FALSE),
            (2, 'group #1', 1, FALSE),
            (3, 'group #2', 2, FALSE),
            (4, 'group #3', 3, TRUE);
    """,
    "component": """
        INSERT INTO
            component (id,name,cad_model_link,vendor_code,supplier_name,weight,price,extra_params)
        VALUES
            (1, 'component #1', 'some-cad-link #1', 'vendor-111', 'supplr#1', 20000.44, 35000.00, '{}'),
            (2, 'component #2', 'some-cad-link #2', 'vendor-112', 'supplr#2', 19000.43, 34000.00, '{}'),
            (3, 'component #3', 'some-cad-link #3', 'vendor-113', 'supplr#3', 18000.42, 33000.00, '{}'),
            (4, 'component #4', 'some-cad-link #4', 'vendor-114', 'supplr#4', 17000.41, 32000.00, '{}');
    """,
    "vehicle": """
        INSERT INTO
            vehicle (id,name,extra_params)
        VALUES
            (1, 'Awesome Car', '{"is_driving_wheel_right": true}');
    """,
    "vehicle_features": """
        INSERT INTO
            vehicle_features (id,vehicle_id,feature_id)
        VALUES
            (1, 1, 1),
            (2, 1, 2),
            (3, 1, 3);
    """,
    "vehicle_configuration": """
        INSERT INTO
            vehicle_configuration (id,vehicle_id,component_id,function_id)
        VALUES
            (1, 1, 1, 1),
            (2, 1, 1, 2),
            (3, 1, 1, 3);
    """
}

_EXECUTION_ORDER = (
    ('group', 'component', 'vehicle'),
    ('feature', 'function'),
    ('vehicle_features', 'vehicle_configuration')
)


def upgrade():
    for _order in _EXECUTION_ORDER:
        for table in _order:
            query = _INSERTS.get(table)
            op.execute(query)


def downgrade():
    for _order in reversed(_EXECUTION_ORDER):
        for table in reversed(_order):
            query = f"DELETE FROM {table};"
            op.execute(query)
