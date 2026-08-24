# Neighborhoods

## Definition

A Neighborhood is one exact, ordered selection of coordinates read when
computing the successor value for a source coordinate.

There are two useful forms:

1. an ordered tuple of relative offsets;
2. a small address function for selection that cannot be expressed as fixed
   offsets.

No region, locus, graph, tile, or neighborhood class hierarchy is needed.

## Shared selector helpers

`ca.selector` is the small coordinate-selection library used to construct
Spaces, Neighborhoods, and structured Seeds. It supplies ordinary functions
for filtering and translating coordinates, composing predicates, measuring
taxicab/Euclidean/Chebyshev distance, selecting balls and shells, following
plain relations, and ordering results.

Selector is not another SimpleProgram field and there is no `Selector` class.
It is reusable mathematical vocabulary beneath the five API concepts.

## Relative offsets

For a t+1D three-cell neighborhood:

```python
neighborhood = (
    (0, -1),
    (0,  0),
    (0,  1),
)
```

The leading zero keeps every read at the current explicit time. Applied at
`(t, x)`, this selects:

```text
(t, x-1), (t, x), (t, x+1)
```

Offsets match the complete coordinate rank. Their order is meaningful because
an exhaustive Rule may distinguish left, self, and right.

Regular metric neighborhoods can be constructed without a semantic class:

```python
neighborhood = neighborhoods.ball(
    spatial_rank=2,
    radius=1,
    metric=selector.taxicab,
)
```

This returns one definite ordered tuple of offsets, each beginning with a zero
time displacement.

## Address functions

Fixed offsets are not required. A relation-based Neighborhood can use ordinary
Seed data:

```python
def adjacent(source, seed):
    t, address = source
    return tuple((t, other) for other in seed.relations["adjacent"][address])
```

This supports `(t, v)` coordinate spaces, irregular adjacencies, and other
address relationships without introducing semantic coordinate types. The
Neighborhood returns coordinates; it does not return graph nodes or region
objects. `ca.neighborhoods.relation(name)` provides this common construction
using the generic relation-following helper from `ca.selector`.

## Division of responsibility

Neighborhood selects candidate read addresses. It does not decide:

- whether an exterior address wraps or has a fixed value—Space resolves that;
- which values are legal—Alphabet decides that;
- what value is emitted—Rule decides that;
- concrete support or relation data—Seed supplies that.

Neighborhood also does not select a set of coordinates to mutate. Each
realized successor coordinate is newly constructed. Logical activity can be
encoded in Alphabet values and interpreted by Rule.

## Reads and the Rule

For each realized source coordinate, execution:

1. asks Neighborhood for ordered addresses;
2. resolves those addresses through Space;
3. gathers their values from the complete current State;
4. calls the exact Rule with those values and the source coordinate.

The source coordinate is available so one ordinary callable can express a law
that depends on address or explicit time when a family truly requires it.

## Plural source

`NEIGHBORHOODS` means an iterable or function yielding definite Neighborhood
values. It may accept Space explicitly because valid offsets and address
functions depend on coordinate rank:

```python
def neighborhoods(space):
    if space.axes == ("t", "x"):
        yield ((0, -1), (0, 0), (0, 1))
```

This is normal Python dependency flow. It does not require a builder protocol
or a semantic family class.
