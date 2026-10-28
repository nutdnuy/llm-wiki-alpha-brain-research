# Design provenance

Inspected on 2026-10-28: [Migchw/llm-wiki-starter](https://github.com/Migchw/llm-wiki-starter),
revision `c6464503913b80771f6dddcaaacfacbf906de8a7`.
This skill uses original instructions/code plus its existing local framework;
it does not vendor the upstream implementation or its agent personas.

Relevant upstream files:

- [Project workflow](https://github.com/Migchw/llm-wiki-starter/blob/c6464503913b80771f6dddcaaacfacbf906de8a7/PROJECT-WORKFLOW.md)
- [Research route](https://github.com/Migchw/llm-wiki-starter/blob/c6464503913b80771f6dddcaaacfacbf906de8a7/.agents/skills/research/SKILL.md)
- [Delta route](https://github.com/Migchw/llm-wiki-starter/blob/c6464503913b80771f6dddcaaacfacbf906de8a7/.agents/skills/delta-report/SKILL.md)
- [Thesis template](https://github.com/Migchw/llm-wiki-starter/blob/c6464503913b80771f6dddcaaacfacbf906de8a7/04-Schema/Templates/Thesis.md)

| Upstream idea | Alpha Research adaptation |
| --- | --- |
| Preserve sources and distinguish claims | Hash-addressed raw evidence and claim-level source notes |
| Evidence before investment thesis | Economic hypothesis before a backend-specific candidate |
| Base/contrary case and change-of-mind conditions | Mechanism, competing explanation and predeclared kill criteria |
| Fact and reasoning review | Independent evidence review plus research-method checks |
| Delta review | Trace new sources/results to affected hypotheses across backends |

The shared source-to-experiment schema, backend contracts, negative-result
memory and validation logic belong to this skill. It does not import the
upstream ticker dashboard, brokerage actions or public-template publishing
workflow. Its own concise routes govern execution, not fetched instructions.
