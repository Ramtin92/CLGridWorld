from unittest import TestCase

from clgridworld.grid_world_actions import GridWorldActions
from clgridworld.grid_world_dynamics import GridWorldDynamics
from clgridworld.grid_world_state import GridWorldStateKey
from tests.grid_world_state_builder import GridWorldStateBuilder


class TestGridWorldDynamics(TestCase):

    def setUp(self):

        self.directional_actions = [GridWorldActions.NORTH, GridWorldActions.EAST, GridWorldActions.SOUTH, GridWorldActions.WEST]
        self.action_names = ["North", "East", "South", "West"]

    def test_new_state_should_be_new_object(self):

        player_coords = (0, 0)
        state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)

        new_state = GridWorldDynamics(state).step(GridWorldActions.NORTH)

        self.assertFalse(state is new_state)

    def test_when_player_moves_into_boundary_should_remain_in_same_state(self):

        grid_shape = (10, 10)
        player_start_coords = [(0, 0), (9, 9), (9, 9), (0, 0)]

        for i in range(len(self.directional_actions)):
            with self.subTest(action=self.action_names[i]):

                player_coords = player_start_coords[i]
                action = self.directional_actions[i]

                state = GridWorldStateBuilder.create_state_with_spec(shape=grid_shape, player_coords=player_coords)
                new_state = GridWorldDynamics(state).step(action)

                self.assertDictEqual(state, new_state)

    def test_when_player_moves_into_empty_space_should_move_into_empty_space(self):

        player_start_coords =           [(1, 0), (0, 0), (0, 0), (0, 1)]
        expected_player_coords_list =   [(0, 0), (0, 1), (1, 0), (0, 0)]

        for i in range(len(self.directional_actions)):
            with self.subTest(action=self.action_names[i]):

                player_coords = player_start_coords[i]
                action = self.directional_actions[i]
                expected_player_coords = expected_player_coords_list[i]

                state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords)
                actual_state = GridWorldDynamics(state).step(action)

                expected_state = state.copy()
                expected_state[GridWorldStateKey.PLAYER_KEY] = expected_player_coords
                self.assertDictEqual(expected_state, actual_state)
                self.assertFalse(actual_state.is_in_pit(), "should not be in pit")

    def test_when_player_moves_into_beacon_should_remain_in_same_state(self):

        shape = (10, 10)
        pit_start_coords = (4, 2)
        pit_end_coords = (4, 7)
        player_start_coords = [(6, 1), (5, 0), (2, 8), (3, 9)]

        for i in range(len(self.directional_actions)):
            with self.subTest(action=self.action_names[i]):

                player_coords = player_start_coords[i]
                action = self.directional_actions[i]

                state = GridWorldStateBuilder.create_state_with_spec(
                    shape=shape, player_coords=player_coords, pit_start_coords=pit_start_coords,
                    pit_end_coords=pit_end_coords)

                new_state = GridWorldDynamics(state).step(action)

                self.assertDictEqual(state, new_state)

    def test_when_player_moves_into_pit_should_move_player_into_pit(self):

        shape = (10, 10)
        pit_start_coords = (4, 2)
        pit_end_coords = (4, 7)
        player_start_coords =         [(5, 4), (4, 1), (3, 2), (4, 8)]
        expected_player_coords_list = [(4, 4), (4, 2), (4, 2), (4, 7)]

        for i in range(len(self.directional_actions)):
            with self.subTest(action=self.action_names[i]):

                player_coords = player_start_coords[i]
                action = self.directional_actions[i]
                expected_player_coords = expected_player_coords_list[i]

                state = GridWorldStateBuilder.create_state_with_spec(
                    shape=shape, player_coords=player_coords, pit_start_coords=pit_start_coords,
                    pit_end_coords=pit_end_coords)

                new_state = GridWorldDynamics(state).step(action)

                expected_state = state.copy()
                expected_state[GridWorldStateKey.PLAYER_KEY] = expected_player_coords
                self.assertDictEqual(expected_state, new_state)
                self.assertTrue(new_state.is_in_pit())

    def test_when_player_moves_into_key_should_remain_in_same_state(self):

        player_start_coords =   [(1, 0), (0, 0), (0, 0), (0, 1)]
        key_start_coords =      [(0, 0), (0, 1), (1, 0), (0, 0)]

        for i in range(len(self.directional_actions)):
            with self.subTest(action=self.action_names[i]):

                player_coords = player_start_coords[i]
                action = self.directional_actions[i]
                key_coords = key_start_coords[i]

                state = GridWorldStateBuilder.create_state_with_spec(player_coords=player_coords, key_coords=key_coords)
                new_state = GridWorldDynamics(state).step(action)

                self.assertDictEqual(state, new_state)
                
    def test_when_player_moves_into_lock_should_remain_in_same_state(self):

        player_start_coords =   [(1, 0), (0, 0), (0, 0), (0, 1)]
        lock_start_coords =      [(0, 0), (0, 1), (1, 0), (0, 0)]

        for i in range(len(self.directional_actions)):
            with self.subTest(action=self.action_names[i]):

                player_coords = player_start_coords[i]
                action = self.directional_actions[i]
                lock_coords = lock_start_coords[i]

                state = GridWorldStateBuilder.create_state_with_spec(
                    player_coords=player_coords, lock_coords=lock_coords)
                new_state = GridWorldDynamics(state).step(action)

                self.assertDictEqual(state, new_state)

    def test_given_player_is_not_near_a_key_when_pick_up_key_should_remain_in_same_state(self):

        shape = (10, 10)
        player_coords = (0, 0)
        key_coords = (9, 9)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, player_coords=player_coords, key_coords=key_coords)
        new_state = GridWorldDynamics(state).step(GridWorldActions.PICK_UP_KEY)

        self.assertDictEqual(state, new_state)

    def test_given_player_is_not_next_to_a_key_when_pick_up_key_should_remain_in_same_state(self):

        shape = (10, 10)
        player_coords = (0, 0)
        key_coords = (1, 1)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, player_coords=player_coords, key_coords=key_coords, lock_coords=None)
        new_state = GridWorldDynamics(state).step(GridWorldActions.PICK_UP_KEY)

        self.assertDictEqual(state, new_state)

    def test_given_player_is_next_to_key_when_pick_up_key_should_pick_up_key(self):

        key_coords = (1, 1)
        player_start_coords = [(0, 1), (1, 2), (2, 1), (1, 0)]
        player_position_to_key = ["North", "East", "South", "West"]

        for i in range(len(player_position_to_key)):
            with self.subTest(player_position_to_key=player_position_to_key[i]):

                player_coords = player_start_coords[i]

                state = GridWorldStateBuilder.create_state_with_spec(
                    player_coords=player_coords, key_coords=key_coords, lock_coords=None)
                actual_state = GridWorldDynamics(state).step(GridWorldActions.PICK_UP_KEY)

                expected_state = state.copy()
                expected_state[GridWorldStateKey.KEY_DICT_KEY] = None
                expected_state[GridWorldStateKey.HAS_KEY_DICT_KEY] = 1
                self.assertDictEqual(expected_state, actual_state)

    def test_given_player_does_not_have_key_and_if_not_next_to_lock_when_unlock_should_remain_in_same_state(self):

        shape = (10, 10)
        player_coords = (0, 0)
        lock_coords = (9, 9)
        key_coords = (0, 9)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, player_coords=player_coords, lock_coords=lock_coords, key_coords=key_coords)
        new_state = GridWorldDynamics(state).step(GridWorldActions.UNLOCK_LOCK)

        self.assertDictEqual(state, new_state)

    def test_given_player_does_not_have_key_and_is_next_to_lock_when_unlock_should_remain_in_same_state(self):

        lock_coords = (1, 1)
        key_coords = (5, 0)
        player_start_coords = [(0, 1), (1, 2), (2, 1), (1, 0)]
        player_position_to_lock = ["North", "East", "South", "West"]

        for i in range(len(player_position_to_lock)):
            with self.subTest(player_position_to_lock=player_position_to_lock[i]):

                player_coords = player_start_coords[i]

                state = GridWorldStateBuilder.create_state_with_spec(
                    player_coords=player_coords, lock_coords=lock_coords, key_coords=key_coords)
                new_state = GridWorldDynamics(state).step(GridWorldActions.UNLOCK_LOCK)

                self.assertDictEqual(state, new_state)

    def test_given_player_has_key_and_if_not_next_to_lock_when_unlock_should_remain_in_same_state(self):

        shape = (10, 10)
        player_coords = (0, 0)
        lock_coords = (9, 9)

        state = GridWorldStateBuilder.create_state_with_spec(
            shape=shape, player_coords=player_coords, lock_coords=lock_coords, key_coords=None)
        new_state = GridWorldDynamics(state).step(GridWorldActions.UNLOCK_LOCK)

        self.assertDictEqual(state, new_state)

    def test_given_player_has_key_and_is_next_to_lock_when_unlock_should_unlock_lock(self):

        lock_coords = (1, 1)
        player_start_coords = [(0, 1), (1, 2), (2, 1), (1, 0)]
        player_position_to_lock = ["North", "East", "South", "West"]

        for i in range(len(player_position_to_lock)):
            with self.subTest(player_position_to_lock=player_position_to_lock[i]):

                player_coords = player_start_coords[i]

                state = GridWorldStateBuilder.create_state_with_spec(
                    player_coords=player_coords, lock_coords=lock_coords, key_coords=None)
                actual_state = GridWorldDynamics(state).step(GridWorldActions.UNLOCK_LOCK)

                expected_state = state.copy()
                expected_state[GridWorldStateKey.LOCK_KEY] = None

                self.assertDictEqual(expected_state, actual_state)
                self.assertTrue(actual_state.has_unlocked_lock(), "lock should be unlocked")
