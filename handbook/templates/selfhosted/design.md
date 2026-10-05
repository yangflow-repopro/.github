<!-- template: selfhosted/design.md v1 -->
<!-- Design language of a self-hosted product: a web UI used at the viewports the product declares, and a native macOS shell. Thirteen H2s, fixed. 'Core symbol' and 'Native shell' are the product slots. -->
# <Name> design language

## Principles

<Five or fewer, each with a consequence.>

## Core symbol

<The product's signature element: what it is, its states, shape and color rules.>

## Color

<Tokens, light and dark (system preference with an in-app override), contrast rules.>

## Typography

<Families (system font stack or self-hosted files; never a third-party font service), sizes, weights, where each is used.>

## Layout and breakpoints

<The spacing scale; the viewports the product declares (`docs/spec.md`), their sizes and how layouts change
between them; touch target sizes.>

## Components

<The shared components, their states, and the rule that screens compose them instead of styling their own.>

## Icons

<Icon source (bundled, never fetched at runtime), sizes, the app and PWA icon set.>

## Motion

<Durations, curves, when motion plays; reduced-motion behaviour.>

## Signature moments

<The few places the product allows itself delight.>

## Copy tone

<Voice, what to avoid, error copy pattern.>

## Accessibility

<Semantic elements, accessible names, keyboard paths, focus order, contrast, the automated check that runs on
every screen.>

## Native shell

<What the macOS shell shows natively (menu bar, window chrome, notifications) and how it matches the web UI.>

## Design acceptance checklist

- [ ] <Every UI PR ticks all items>
