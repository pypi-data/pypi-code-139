"""
topologies (self, collection, Agent)

    self       - for additional parameters, such as n_size for ring_topology.
    agent      - The current agent in the collection.
    collection - A collection of agents that make up the network.
"""
from cify.core.base_classes.agent import Agent
from cify.core.base_classes.collection import Collection

__all__ = ['star_topology', 'ring_topology']


# star topology
def star_topology(agent: Agent, collection: Collection, **kwargs):

    """
    Standard star topology where all :class:`Agent` s are connected with each other.

    :param agent: The current agent in the :class:`Collection`.
    :type agent: :class:`Agent`
    :param collection: The collection containing the :class:`Agent`.
    :type collection: :class:`Collection`
    """

    # FIXME: Currently only works for Particles!!!

    best_pos = agent.social_best_pos
    for p in collection:
        if agent.obj_func.cmp(p.position.value, best_pos.value):
            best_pos = p.position
    agent.social_best_pos = best_pos.copy()

    # if particle.obj_func.cmp(particle.p_best_position.value, particle.social_best_pos.value):
    #     particle.social_best_pos = particle.p_best_position
    # else:
    #     particle.social_best_pos = kwargs['self'].global_optimum_pos


# ring topology
def ring_topology(agent: Agent, collection: Collection,
                  n_size: int = 3,
                  **kwargs):
    """
    Ring topology where all :class:`Agent` s are connected to the :class:`Agent` s located near them in the
    :class:`Collection`.

    :param agent: The current agent in the :class:`Collection`.
    :type agent: :class:`Agent`
    :param collection: The collection containing the :class:`Agent`.
    :type collection: :class:`Collection`
    :param n_size: The size of the neighbourhood to use.
    :type n_size: int, optional
    """
    # find Agent in Collections
    index = 0
    for i in range(len(collection)):
        if agent == collection[i]:
            index = i
            break

    eax = int(n_size / 2)
    for i in range(n_size):
        if index - eax < 0:
            if (
                agent.p_best_position
                < collection[len(collection) - eax + index].social_best_pos
            ):
                collection[
                    len(collection) - eax + index
                ].social_best_pos = agent.p_best_position
        elif index - eax > len(collection) - 1:
            if (
                agent.p_best_position
                < collection[index - eax - len(collection)].social_best_pos
            ):
                collection[
                    index - eax - len(collection)
                ].social_best_pos = agent.p_best_position
        else:
            if agent.p_best_position < collection[index - eax].social_best_pos:
                collection[index - eax].social_best_pos = agent.p_best_position
        eax -= 1


# def von_neumann_topology(**kwargs):
#     pass


# def pyramid_topology(**kwargs):
#     pass


# def clusters_topology(**kwargs):
#     pass


# def wheel_topology(**kwargs):
#     pass
