---
description: Configure and tune search so agents and customers find useful answers quickly.
icon: magnifying-glass
---

# Intelligent Search

Intelligent search is the bridge between a large knowledge repository and a fast answer experience.

{% tabs %}
{% tab title="Relevance" %}
Use product, audience, language, article type, and freshness signals to prioritize the best answer.
{% endtab %}

{% tab title="Recommendations" %}
Surface suggested articles in agent workflows based on service request context and customer intent.
{% endtab %}

{% tab title="Analysis" %}
Review search terms, no-result queries, clicked answers, and deflection outcomes to tune the repository.
{% endtab %}
{% endtabs %}

```mermaid
flowchart LR
  Query[Customer or agent question] --> Index[Knowledge index]
  Index --> Rank[Relevance and filters]
  Rank --> Answer[Article, excerpt, or recommendation]
  Answer --> Analytics[Search and answer analysis]
  Analytics --> Rank
```
