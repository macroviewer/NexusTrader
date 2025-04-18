import pytest
import asyncio
from nexustrader.core.entity import TaskManager


@pytest.mark.asyncio
async def test_task_creation_and_execution(task_manager: TaskManager) -> None:
    result = []

    async def sample_task():
        await asyncio.sleep(0.1)
        result.append(1)

    task = task_manager.create_task(sample_task())
    await task

    assert result == [1]
    assert not task_manager._tasks  # Task should be removed after completion


@pytest.mark.asyncio
async def test_task_cancellation(task_manager: TaskManager) -> None:
    async def long_running_task():
        try:
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            return "cancelled"

    task = task_manager.create_task(long_running_task())
    await asyncio.sleep(0.1)
    await task_manager.cancel()

    assert not task_manager._tasks  # expect result is empty as _tasks be removed
    # assert task.cancelled()
    assert task.done()

    # await asyncio.sleep(5)

    # assert not task_manager._tasks
    # assert task.done()
