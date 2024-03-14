# prooompt-engineer

We can do variable templating like in Jinja2...

```simple/template.txt
{% message system %}
You are a genius
{% endmessage %}

{% message user %}
My name is {{name}}. What is my name?
{% endmessage %}
```

```simple/template.json
[
  {
    "type": "message",
    "role": "system",
    "template": [
      {
        "type": "text",
        "content": "You are a genius"
      }
    ]
  },
  {
    "type": "message",
    "role": "user",
    "template": [
      {
        "type": "text",
        "content": "My name is "
      },
      {
        "type": "eval",
        "value": "name"
      },
      {
        "type": "text",
        "content": ". What is my name?"
      }
    ]
  }
]
```

We can evaluate python expressions...

```eval/template.txt
{% message user %}
Alpha is {{alpha}}. Beta plus one is {{beta+1}}. Express {{alpha + 2 * beta}} in terms of alpha and beta.
{% endmessage %}
```

```eval/template.json
[
  {
    "type": "message",
    "role": "user",
    "template": [
      {
        "type": "text",
        "content": "Alpha is "
      },
      {
        "type": "eval",
        "value": "alpha"
      },
      {
        "type": "text",
        "content": ". Beta plus one is "
      },
      {
        "type": "eval",
        "value": "beta+1"
      },
      {
        "type": "text",
        "content": ". Express "
      },
      {
        "type": "eval",
        "value": "alpha + 2 * beta"
      },
      {
        "type": "text",
        "content": " in terms of alpha and beta."
      }
    ]
  }
]
```

We can define loops within our prompts...

```loop.txt
{% message user %}
I have three friends:

{% for friend in friends %}
- {{friend.name}} aged {{friend.age}}
{% endfor %}

Who is the oldest?
{% endmessage %}
```

```loop.json
  [
    {
      "type": "message",
      "role": "user",
      "template": [
        {
          "type": "text",
          "content": "I have three friends:\n"
        },
        {
          "type": "loop",
          "content": "name",
          "iterator": "friend",
          "iterable": "friends",
          "template": [
            {
              "type": "text",
              "content": "\n- "
            },
            {
              "type": "eval",
              "value": "friend['name']"
            },
            {
              "type": "text",
              "content": " aged "
            },
            {
              "type": "eval",
              "value": "friend['age']"
            }
          ]
        },
        {
          "type": "text",
          "content": "\n\nWho is the oldest?"
        }
      ]
    }
  ]
```

We can define loops outside our prompts (to get few shot templates 🙀)...

```loop_outer.txt
{% for example in few_shot_examples %}

    {% message user %}
    What is {{example.alpha}} + {{example.beta}}?
    {% endmessage %}

    {% message assistant %}
    {{example.alpha + example.beta}}
    {% endmessage %}

{% endfor %}

{% message user %}
What is {{gamma}} + {{delta}}?
{% endmessage %}
```

```loop_outer.json
[{
    "type": "loop",
    "content": "example",
    "iterator": "example",
    "iterable": "few_shot_examples",
    "template": [{
        "type": "message",
        "role": "user",
        "template": [{
            "type": "text",
            "content": "What is "
        }, {
            "type": "eval",
            "value": "example.alpha"
        }, {
            "type": "text",
            "content": " + "
        }, {
            "type": "eval",
            "value": "example.beta"
        }, {
            "type": "text",
            "content": "?"
        }]
    }, {
        "type": "message",
        "role": "assistant",
        "template": [{
            "type": "eval",
            "value": "example.alpha + example.beta"
        }]
    }]
}, {
    "type": "message",
    "role": "user",
    "template": [{
        "type": "text",
        "content": "What is "
    }, {
        "type": "eval",
        "value": "gamma"
    }, {
        "type": "text",
        "content": " + "
    }, {
        "type": "eval",
        "value": "delta"
    }, {
        "type": "text",
        "content": "?"
    }]
}]
```
