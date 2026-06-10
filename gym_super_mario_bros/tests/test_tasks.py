"""Tests for registered Mario task metadata."""
from unittest import TestCase

from ..tasks import MarioTask
from ..tasks import all_tasks
from ..smb3_stages import SMB3_STAGES_PER_WORLD
from ..smb3_stages import SMB3_VALIDATED_STAGES
from ..smb3_stages import smb3_stage_matrix
from ..tasks import task_for_config
from ..tasks import task_for_env_id
from ..tasks import task_ids


class ShouldExposeRegisteredTaskMetadata(TestCase):
    """Test task metadata helpers for the current environment surface."""

    def test_task_inventory_matches_registered_env_surface(self):
        canonical_tasks = all_tasks()
        all_env_ids = task_ids(include_aliases=True)

        self.assertEqual(112, len(canonical_tasks))
        self.assertEqual(144, len(all_env_ids))
        self.assertIn('SuperMarioBros-v0', all_env_ids)
        self.assertIn('SuperMarioBros1-1-v0', all_env_ids)
        self.assertIn('SuperMarioBros2-D-4-v0', all_env_ids)
        self.assertIn('SuperMarioBros2USA-7-2-v0', all_env_ids)
        self.assertIn('SuperMarioBros3-1-1-v0', all_env_ids)
        self.assertIn('SuperMarioBros3-1-6-v0', all_env_ids)
        self.assertNotIn('SuperMarioBrosRandomStages-v0', all_env_ids)

    def test_task_lookup_by_env_id(self):
        task = task_for_env_id('SuperMarioBros2-A-2-v0')

        self.assertIsInstance(task, MarioTask)
        self.assertEqual('lost_levels', task.game)
        self.assertEqual(10, task.world)
        self.assertEqual('A', task.world_label)
        self.assertEqual(2, task.stage)
        self.assertTrue(task.single_stage)
        self.assertEqual(task.env_id, task.task_id)

    def test_aliases_point_to_canonical_task_id(self):
        task = task_for_env_id('SuperMarioBros1-1-v0')

        self.assertEqual('SuperMarioBros-1-1-v0', task.task_id)
        self.assertEqual('SuperMarioBros-1-1-v0', task.alias_of)

    def test_config_lookup_returns_canonical_tasks(self):
        self.assertEqual(
            'SuperMarioBros-v0',
            task_for_config('smb1', 0).env_id,
        )
        self.assertEqual(
            'SuperMarioBros-4-2-v0',
            task_for_config('smb1', 0, world=4, stage=2).env_id,
        )
        self.assertEqual(
            'SuperMarioBros2USA-7-2-v0',
            task_for_config('smb2_usa', 0, world=7, stage=2).env_id,
        )
        self.assertEqual(
            'SuperMarioBros3-1-4-v0',
            task_for_config('smb3', 0, world=1, stage=4).env_id,
        )

    def test_filters_are_available_for_eval_matrices(self):
        stage_tasks = all_tasks(single_stage=True)
        smb3_tasks = all_tasks(game_family='smb3')

        self.assertEqual(108, len(stage_tasks))
        self.assertEqual(
            (
                'SuperMarioBros3-v0',
                'SuperMarioBros3-1-1-v0',
                'SuperMarioBros3-1-2-v0',
                'SuperMarioBros3-1-4-v0',
                'SuperMarioBros3-1-6-v0',
            ),
            tuple(task.env_id for task in smb3_tasks),
        )
        self.assertRaises(ValueError, all_tasks, split='unknown')


class ShouldExposeSuperMarioBros3StageMatrix(TestCase):
    """Test the conservative SMB3 numbered-course catalog."""

    def test_matrix_covers_numbered_courses(self):
        stages = smb3_stage_matrix()

        self.assertEqual(sum(SMB3_STAGES_PER_WORLD), len(stages))
        self.assertEqual(
            ('SuperMarioBros3-1-1-v0', 'SuperMarioBros3-1-2-v0'),
            tuple(stage.env_id for stage in stages[:2]),
        )
        self.assertEqual('SuperMarioBros3-8-2-v0', stages[-1].env_id)

    def test_validated_filter_matches_registered_entry_recipes(self):
        stages = smb3_stage_matrix(validated=True)

        self.assertEqual(SMB3_VALIDATED_STAGES, tuple(stage.target for stage in stages))
