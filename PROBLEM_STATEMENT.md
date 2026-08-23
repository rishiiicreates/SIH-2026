# Problem Statement — SIH 2026

**PS ID:** 26108
**Title:** AI-Powered Recommendation Engine for Identifying Applicable
Indian Standards for Procurement Specifications

## Original text (verbatim, source of truth)

> Background Government departments, Public Sector Enterprises
> (PSEs), procurement agencies, and private organizations procure a
> wide range of products and services through e-procurement portals.
> Procurement officials are often required to prepare technical
> specifications that reference the appropriate Indian Standards
> (IS). However, identifying the correct standard(s) is challenging
> due to the large number of published standards, overlapping
> scopes, frequent revisions, and the need to consider associated or
> normative reference standards. Consequently, tender specifications
> may omit relevant standards, reference outdated versions, or
> include incomplete technical requirements, leading to ambiguity,
> reduced product quality, and procurement disputes.
>
> An intelligent system is required that can automatically analyze a
> product description or technical specification and recommend the
> most relevant Indian Standard(s), along with allied,
> cross-referenced, or normative standards that should also be
> considered.
>
> Description Develop an AI-powered recommendation engine that
> integrates with procurement portals and assists procurement
> officials in identifying the most relevant Indian Standards and
> related standards while preparing tender specifications.
>
> Expected Features
> - Accept product descriptions, technical specifications, or tender
>   documents as input.
> - Recommend the most relevant Indian Standard(s) based on semantic
>   understanding rather than keyword matching.
> - Identify allied standards, including normative references, test
>   methods, terminology standards, safety standards, installation
>   standards, and related product standards.
> - Highlight the latest published version and amendments of the
>   recommended standards.
> - Suggest mandatory certification requirements, where applicable
>   (e.g., BIS Product Certification, CRS, Hallmarking).
> - Support multilingual input and natural language queries.

The sections below are the same content organized for quick reference
during planning — use the verbatim text above if wording precision
matters (e.g., quoting in the pitch deck).

## Background

Government departments, PSEs, procurement agencies, and private
organizations procure a wide range of products and services through
e-procurement portals. Procurement officials must prepare technical
specifications that reference the appropriate Indian Standards (IS).
Identifying the correct standard(s) is hard because of:

- a large number of published standards
- overlapping scopes between standards
- frequent revisions/amendments
- the need to consider associated or normative reference standards

This leads to tenders that omit relevant standards, cite outdated
versions, or have incomplete technical requirements — causing
ambiguity, reduced product quality, and procurement disputes.

## What's needed

A system that automatically analyzes a product description or
technical specification and recommends the most relevant Indian
Standard(s), along with allied, cross-referenced, or normative
standards that should also be considered.

## Description

An AI-powered recommendation engine that integrates with procurement
portals and assists procurement officials in identifying the most
relevant Indian Standards and related standards while preparing
tender specifications.

## Expected Features (this is the actual scoring checklist)

1. Accept product descriptions, technical specifications, or tender
   documents as input.
2. Recommend the most relevant Indian Standard(s) based on **semantic
   understanding rather than keyword matching**.
3. Identify allied standards, including normative references, test
   methods, terminology standards, safety standards, installation
   standards, and related product standards.
4. Highlight the latest published version and amendments of the
   recommended standards.
5. Suggest mandatory certification requirements, where applicable
   (e.g., BIS Product Certification, CRS, Hallmarking).
6. Support multilingual input and natural language queries.

## Why this matters for scope decisions

Every feature we build should trace back to one of the six items
above. If a proposed feature doesn't map to one of these, it's likely
scope creep — however impressive it sounds. See ROADMAP.md for how
these six map to our build phases.
