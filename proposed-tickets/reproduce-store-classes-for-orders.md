---
title: "Reproduce store classes for orders"
labels: [type::feature, "area::orders"]
weight: 3
---

> **Feature** — The orders service gains a store layer reproduced from inventory-service's store classes.

## Context

The orders service needs the store layer that inventory-service already runs, under the orders namespace.

## Scope

- An orders store layer with the class structure and converter logic of inventory-service's store classes.
- Package names under the orders service's namespace.

## Implementation Approach

Take the class structure and converter logic from inventory-service's [`BaseRecord`](https://code.example.com/inventory/BaseRecord.java) and [`StoreConfig`](https://code.example.com/inventory/StoreConfig.java). Change package names from `com.example.inventory` to `com.example.orders`. Bring along anything these classes reference.

## Testing

- A record round-trips through the orders store with its converter logic applied.

## Acceptance Criteria

- [ ] An orders record round-trips through the store with converter logic applied
- [ ] All store classes are under the `com.example.orders` package
