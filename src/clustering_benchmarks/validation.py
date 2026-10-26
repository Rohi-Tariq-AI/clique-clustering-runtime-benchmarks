from __future__ import annotations


def first_clusters_equal(partitioning, overlapping) -> bool:
    if not partitioning.clusters or not overlapping.clusters:
        return not partitioning.clusters and not overlapping.clusters
    p = partitioning.clusters[0]
    o = overlapping.clusters[0]
    return (
        set(p.nodes) == set(o.nodes)
        and set(p.internal_edges) == set(o.internal_edges)
        and set(p.external_edges) == set(o.external_edges)
        and p.relative_density == o.relative_density
    )


def disjoint_starting_triangles(overlapping) -> bool:
    earlier_nodes = set()
    for cluster in overlapping.clusters:
        if not set(cluster.starting_triangle).isdisjoint(earlier_nodes):
            return False
        earlier_nodes.update(cluster.nodes)
    return True


def density_states_consistent(result) -> bool:
    for cluster in result.clusters:
        denominator = len(cluster.internal_edges) + len(cluster.external_edges)
        calculated = round(len(cluster.internal_edges) / denominator, 2) if denominator else 0.0
        if calculated != cluster.relative_density:
            return False
    return True
