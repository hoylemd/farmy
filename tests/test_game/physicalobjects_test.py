from game.physicalobjects import InertialObject
from game import resources
from mock import MagicMock


def test_InertialObject_init__motionless():
    sut = InertialObject(img=resources.chevron_image)

    assert sut.velocity_x == 0.0
    assert sut.velocity_y == 0.0
    assert sut.rotation_speed == 0.0


def test_InertialObject_update__motionless():
    sut = InertialObject(img=resources.chevron_image)

    sut.x = 23.45
    sut.y = 123.34

    sut.velocity_x = 0.0
    sut.velocity_y = 0.0

    sut.update(1.0)

    assert sut.x == 23.45
    assert sut.y == 123.34


def test_InertialObject_update__forward():
    sut = InertialObject(img=resources.chevron_image)

    sut.x = 23.45
    sut.y = 123.34

    sut.velocity_x = 10.0
    sut.velocity_y = 0.0

    sut.update(1.0)

    assert sut.x == 33.45
    assert sut.y == 123.34


def test_InertialObject_update__diagonal():
    sut = InertialObject(img=resources.chevron_image)

    sut.x = 23.45
    sut.y = 123.34

    sut.velocity_x = 10.0
    sut.velocity_y = -5.0

    sut.update(1.0)

    assert sut.x == 33.45
    assert sut.y == 118.34


def test_InertialObject_update__partial_dt():
    sut = InertialObject(img=resources.chevron_image)

    sut.x = 23.45
    sut.y = 123.34

    sut.velocity_x = 10.0
    sut.velocity_y = -5.0

    sut.update(0.5)

    assert sut.x == 28.45
    assert sut.y == 120.84


def test_InertialObject_update__motionless_rotation():
    sut = InertialObject(img=resources.chevron_image)

    sut.rotation = 0.0

    sut.rotation_speed = 0.0

    sut.update(1.0)

    assert sut.rotation == 0.0


def test_InertialObject_update__positive_rotation():
    sut = InertialObject(img=resources.chevron_image)

    sut.rotation = 0.0

    sut.rotation_speed = 6.0

    sut.update(1.0)

    assert sut.rotation == 6.0


def test_InertialObject_update__negative_rotation():
    sut = InertialObject(img=resources.chevron_image)

    sut.rotation = 0.0

    sut.rotation_speed = -15.0

    sut.update(1.0)

    assert sut.rotation == 345.0


def test_InertialObject_update__rotation_partial_dt():
    sut = InertialObject(img=resources.chevron_image)

    sut.rotation = 0.0

    sut.rotation_speed = -10.0

    sut.update(0.5)

    assert sut.rotation == 355.0


class Collider(InertialObject):
    def __init__(self, *args, **kwargs):
        super(Collider, self).__init__(img=resources.chevron_image,
                                       damaging=True, *args, **kwargs)


class Target(InertialObject):
    def __init__(self, *args, **kwargs):
        super(Target, self).__init__(img=resources.chevron_image,
                                     vulnerable=True, *args, **kwargs)


def test_InertialObject_collides_with__no_collision():
    sut = Target()
    collider = Collider()

    sut.x = 200.0
    sut.y = 300.0

    collider.x = sut.x + ((sut.width + collider.width) / 2.0 + 10)
    collider.y = sut.y

    assert not sut.collides_with(collider)


def test_InertialObject_collides_with__collision_not_vulnerable():
    sut = Collider()
    collider = Collider()

    sut.x = 200.0
    sut.y = 300.0

    collider.x = sut.x + ((sut.width + collider.width) / 2.0 - 10)
    collider.y = sut.y

    assert not sut.collides_with(collider)


def test_InertialObject_collides_with__collision_not_damaging():
    sut = Target()
    collider = Target()

    sut.x = 200.0
    sut.y = 300.0

    collider.x = sut.x + ((sut.width + collider.width) / 2.0 - 10)
    collider.y = sut.y

    assert not sut.collides_with(collider)


def test_InertialObject_collides_with__collision_with_flags():
    sut = Target()
    collider = Collider()

    sut.x = 200.0
    sut.y = 300.0

    collider.x = sut.x + ((sut.width + collider.width) / 2.0 - 10)
    collider.y = sut.y

    assert sut.collides_with(collider)


def test_InertialObject_die():
    sut = InertialObject(img=resources.chevron_image)

    assert not sut.dead

    sut.die()

    assert sut.dead


def test_InertialObject_handleCollision__calls_die():
    sut = Target()
    collider = Collider()

    sut.die = MagicMock()

    sut.handle_collision(collider)

    assert sut.die.called


def test_InertialObject_handleCollision__ignores_same_object_type():
    sut = InertialObject(img=resources.chevron_image)
    collider = InertialObject(img=resources.asteroid_image)

    sut.die = MagicMock()

    sut.handle_collision(collider)

    assert not sut.die.called
