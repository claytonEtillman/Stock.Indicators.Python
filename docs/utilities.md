---
title: Utilities and Helpers
permalink: /utilities/
layout: default
---

# {{ page.title }}

## Utilities for indicator results

### Convert to quotes

`results.to_quotes()` will transform indicator results back into an `list[Quote]` so it can be re-used to generate an [indicator of indicators]({{site.baseurl}}/guide/#generating-indicator-of-indicators).

```python
# example: an SMA of RSI
results = indicators.get_rsi(quotes)
quotes_from_rsi = results.to_quotes()
sma_of_rsi = indicators.get_sma(quotes_from_rsi, 20)

```

Currently, `.to_quotes()` is only available on a select few indicators.  If you find an indicator that is a good candidate for this utility, please [submit an Issue]({{site.baseurl}}/contributing/#reporting-bugs-and-feature-requests).

:warning: WARNING! In many cases, `.to_quotes()` will remove any `None` results -- this will produce fewer historical `quotes` than were originally provided.

### Find indicator result by date

`results.find(lookup_date)` is a simple lookup for your indicator results collection.  Just specify the date you want returned.

```python
# fetch historical quotes from your favorite feed
quotes = get_history_from_feed("MSFT")

# calculate indicator series
results = indicators.get_ema(quotes, 20)

# find result on a specific date
from datetime import datetime
lookup_date = datetime(2018, 10, 12)
result = results.find(lookup_date)

```

### Remove warmup periods

`results.remove_warmup_periods()` will remove the recommended initial warmup periods from indicator results.
An alternative `.remove_warmup_periods(remove_periods)` is also provided if you want to customize the pruning amount.

```python
# auto remove recommended warmup periods
results = indicators.get_ema(quotes, 20).remove_warmup_periods()

# remove user-specific quantity of periods
results = indicators.get_ema(quotes, 20).remove_warmup_periods(10)

```

See [individual indicator pages]({{site.baseurl}}/indicators/#content) for information on recommended pruning quantities.

:warning: Note: `.remove_warmup_periods()` is not available on indicators that do not have any recommended pruning; however, you can still do a custom pruning by using the customizable `.remove_warmup_periods(remove_periods)`.

:warning: WARNING! `.remove_warmup_periods()` will reverse-engineer some parameters in determing the recommended pruning amount.  Consequently, on rare occassions when there are unusual results, there can be an erroneous increase in the amount of pruning.  If you want more certainty, use the `.remove_warmup_periods(remove_periods)` with a specific number of `remove_periods`.