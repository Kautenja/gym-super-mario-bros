"""A method to decode target values for a ROM stage environment."""


def decode_target(target, lost_levels):
    """
    Return the target area for target world and target stage.

    Args:
        target_world (None, int): the world to target
        target_stage (None, int): the stage to target
        lost_levels (bool): whether to use lost levels game

    Returns (int):
        the area to target to load the target world and stage

    """
    # Type and value check the lost levels parameter
    if not isinstance(lost_levels, bool):
        raise TypeError('lost_levels must be of type: bool')
    # if there is no target, the world, stage, and area targets are all None
    if target is None:
        return None, None, None
    elif not isinstance(target, tuple):
        raise TypeError('target must be  of type tuple')
    # unwrap the target world and stage
    target_world, target_stage = target
    # Type and value check the target world parameter
    if not isinstance(target_world, int):
        raise TypeError('target_world must be of type: int')
    else:
        if lost_levels:
            if not 1 <= target_world <= 12:
                raise ValueError('target_world must be in {1, ..., 12}')
        elif not 1 <= target_world <= 8:
            raise ValueError('target_world must be in {1, ..., 8}')
    # Type and value check the target level parameter
    if not isinstance(target_stage, int):
        raise TypeError('target_stage must be of type: int')
    else:
        if not 1 <= target_stage <= 4:
            raise ValueError('target_stage must be in {1, ..., 4}')

    # no target are defined for no target world or stage situations
    if target_world is None or target_stage is None:
        return None
    # setup target area if target world and stage are specified
    target_area = target_stage
    # setup the target area depending on whether this is SMB 1 or 2
    if lost_levels:
        # setup the target area depending on the target world and stage
        if target_world in {1, 3}:
            if target_stage >= 2:
                target_area = target_area + 1
        elif target_world >= 5:
            # TODO: figure out why all worlds greater than 5 fail.
            # target_area = target_area + 1
            # for now just raise a value error
            worlds = set(range(5, 12 + 1))
            msg = 'lost levels worlds {} not supported'.format(worlds)
            raise ValueError(msg)
    else:
        # setup the target area depending on the target world and stage
        if target_world in {1, 2, 4, 7}:
            if target_stage >= 2:
                target_area = target_area + 1

    return target_world, target_stage, target_area


# explicitly define the outward facing API of this module
__all__ = [decode_target.__name__]
