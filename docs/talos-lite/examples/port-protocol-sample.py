"""插座（Protocol）与可插拔转接头（Adapter）最小教学示例。"""

from contextlib import contextmanager
from typing import Iterator, Protocol


class LockPort(Protocol):
    """【墙上国标插座】核心业务只认这份标准，不关心电脑系统细节。"""

    @contextmanager
    def acquire(self, resource_id: str) -> Iterator[None]: ...


class MemoryFakeLock:
    """【测试用假插头】不碰硬盘，毫秒级验证并发冲突逻辑。"""

    def __init__(self) -> None:
        self.active: set[str] = set()

    @contextmanager
    def acquire(self, resource_id: str) -> Iterator[None]:
        if resource_id in self.active:
            raise RuntimeError(f"锁已被占用: {resource_id}")
        self.active.add(resource_id)
        try:
            yield
        finally:
            self.active.remove(resource_id)


def update_project_summary(lock: LockPort, project_id: str, new_text: str) -> str:
    """【纯业务大脑】只接收插座，永远不直接 import 操作系统锁或数据库。"""
    with lock.acquire(project_id):
        return f"[{project_id}] 已安全更新摘要: {new_text}"
