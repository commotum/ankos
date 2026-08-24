# Neighborhoods

## Definition

A Neighborhood is one exact, ordered selection of spatial addresses read when
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
    (-1,),
    ( 0,),
    ( 1,),
)
```

Neighborhood offsets contain only spatial displacement. Applied at `(t, x)`,
this selects:

```text
(t, x-1), (t, x), (t, x+1)
```

The executor preserves the source time while translating the spatial address.
Time remains explicit in the resulting State coordinates; it is simply not
repeated as a meaningless zero in every Neighborhood constant. Offset rank is
therefore `len(space.axes) - 1`. Order remains meaningful because an exhaustive
Rule may distinguish left, self, and right.

Regular metric neighborhoods can be constructed without a semantic class:

```python
neighborhood = neighborhoods.ball(
    spatial_rank=2,
    radius=1,
    metric=selector.taxicab,
)
```

This returns one definite ordered tuple of two-component spatial offsets.

## Address functions

Fixed offsets are not required. A relation-based Neighborhood can use ordinary
Seed data:

```python
def adjacent(spatial, seed):
    (address,) = spatial
    return tuple((other,) for other in seed.relations["adjacent"][address])
```

This supports `(t, v)` coordinate spaces, irregular adjacencies, and other
address relationships without introducing semantic coordinate types. The
Neighborhood accepts and returns spatial addresses; the resolver preserves the
current explicit time when it forms full State coordinates. It does not return
graph nodes or region objects. `ca.neighborhoods.relation(name)` provides this
common construction using the generic relation-following helper from
`ca.selector`.

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

1. gives Neighborhood the source's spatial address;
2. restores the current time and resolves the selected addresses through
   Space;
3. gathers their values from the complete current State;
4. calls the exact Rule with those ordered values.

The default Rule contract is deliberately only `observed -> value`. If a
concrete family later demonstrates that its law requires coordinate or time
context, that can be added as a focused extension instead of taxing every local
rule in advance.

## Optional plural source

Use a plural Neighborhood source only when several Neighborhoods are actually
being studied. It may accept Space explicitly because valid spatial offsets
and address functions depend on coordinate rank:

```python
def neighborhoods(space):
    if space.axes == ("t", "x"):
        yield ((-1,), (0,), (1,))
```

For ECA, left/self/right is one fixed Neighborhood, so the catalog module
exposes it as a constant instead. This is normal Python dependency flow. It
does not require a builder protocol or a semantic family class.
