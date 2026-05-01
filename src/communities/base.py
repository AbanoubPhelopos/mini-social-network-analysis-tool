from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CommunityResult:
    """Container for community detection results."""

    algorithm: str
    labels: Dict[Any, int]
    num_communities: int
    modularity: float
    execution_time: float
    community_sizes: Dict[int, int]
    iteration_data: Dict[str, Any] = field(default_factory=dict)

    def get_community_sizes_list(self) -> List[int]:
        """Return community sizes as a sorted list (descending)."""
        return sorted(self.community_sizes.values(), reverse=True)
