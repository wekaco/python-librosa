# python-librosa

## Operations

## `griffinlim`

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgbG9hZFsvTG9hZCB3YXYvXSAtLT58eXxzcGVjdG9ncmFtW1NwZWN0b2dyYW1dXG4gIHNwZWN0b2dyYW0tLT58U3xncmlmZmlubGltW2dyaWZmaW5saW1dXG4gIGxvYWQtLT58eXxjaGFubmVsX21lcmdlcltjaGFubmVsX21lcmdlcl1cbiAgZ3JpZmZpbmxpbS0tPnx5fGNoYW5uZWxfbWVyZ2VyXG4gIGNoYW5uZWxfbWVyZ2VyLS0-fHl8d3JpdGVbL1dyaXRlIHdhdi9dIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggTFJcbiAgbG9hZFsvTG9hZCB3YXYvXSAtLT58eXxzcGVjdG9ncmFtW1NwZWN0b2dyYW1dXG4gIHNwZWN0b2dyYW0tLT58U3xncmlmZmlubGltW2dyaWZmaW5saW1dXG4gIGxvYWQtLT58eXxjaGFubmVsX21lcmdlcltjaGFubmVsX21lcmdlcl1cbiAgZ3JpZmZpbmxpbS0tPnx5fGNoYW5uZWxfbWVyZ2VyXG4gIGNoYW5uZWxfbWVyZ2VyLS0-fHl8d3JpdGVbL1dyaXRlIHdhdi9dIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)

```mermaid
graph LR
  load[/Load wav/] -->|y|spectogram[Spectogram]
  spectogram-->|S|griffinlim[griffinlim]
  load-->|y|channel_merger[channel_merger]
  griffinlim-->|y|channel_merger
  channel_merger-->|y|write[/Write wav/]
```

## `griffinlim_filter`

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgbG9hZFsvTG9hZCB3YXYvXSAtLT58eXxzcGVjdG9ncmFtW1NwZWN0b2dyYW1dXG4gIHNwZWN0b2dyYW0tLT58U3x6ZXJvc19ocFtaZXJvID4gZm1pbl1cbiAgemVyb3NfaHAgLS0-fFN8Z3JpZmZpbmxpbV9ocFtncmlmZmlubGltXVxuICBncmlmZmlubGltX2hwLS0-fHl8Y2hhbm5lbF9tZXJnZXJcblxuICBzcGVjdG9ncmFtLS0-fFN8emVyb3NfbHBbWmVybyA8IGZtaW5dXG4gIHplcm9zX2xwIC0tPnxTfGdyaWZmaW5saW1fbHBbZ3JpZmZpbmxpbV1cbiAgZ3JpZmZpbmxpbV9scC0tPnx5fGNoYW5uZWxfbWVyZ2VyXG5cbiAgY2hhbm5lbF9tZXJnZXItLT58eXx3cml0ZVsvV3JpdGUgd2F2L10iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggTFJcbiAgbG9hZFsvTG9hZCB3YXYvXSAtLT58eXxzcGVjdG9ncmFtW1NwZWN0b2dyYW1dXG4gIHNwZWN0b2dyYW0tLT58U3x6ZXJvc19ocFtaZXJvID4gZm1pbl1cbiAgemVyb3NfaHAgLS0-fFN8Z3JpZmZpbmxpbV9ocFtncmlmZmlubGltXVxuICBncmlmZmlubGltX2hwLS0-fHl8Y2hhbm5lbF9tZXJnZXJcblxuICBzcGVjdG9ncmFtLS0-fFN8emVyb3NfbHBbWmVybyA8IGZtaW5dXG4gIHplcm9zX2xwIC0tPnxTfGdyaWZmaW5saW1fbHBbZ3JpZmZpbmxpbV1cbiAgZ3JpZmZpbmxpbV9scC0tPnx5fGNoYW5uZWxfbWVyZ2VyXG5cbiAgY2hhbm5lbF9tZXJnZXItLT58eXx3cml0ZVsvV3JpdGUgd2F2L10iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)

```mermaid
graph LR
  load[/Load wav/] -->|y|spectogram[Spectogram]
  spectogram-->|S|zeros_hp[Zero > fmin]
  zeros_hp -->|S|griffinlim_hp[griffinlim]
  griffinlim_hp-->|y|channel_merger

  spectogram-->|S|zeros_lp[Zero < fmin]
  zeros_lp -->|S|griffinlim_lp[griffinlim]
  griffinlim_lp-->|y|channel_merger

  channel_merger-->|y|write[/Write wav/]
```

## `hpss`

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgbG9hZC0tPnx5fHJlc2lkdWFsW3kgLSB4XVxuICBsb2FkWy9Mb2FkIHdhdi9dIC0tPnx5fGhhcm1vbmljW2hhcm1vbmljXVxuICBoYXJtb25pYy0tPnx5fHdyaXRlXzBbL1dyaXRlIHdhdi9dXG5cbiAgaGFybW9uaWMgLS0-fHl8YWRkW3kgKyB4XVxuICBsb2FkIC0tPnx5fHBlcmNbcGVyY3Vzc2l2ZV1cbiAgcGVyYyAtLT58eHxhZGRbeSArIHhdXG4gIGFkZCAtLT4gfHh8cmVzaWR1YWxcbiAgcmVzaWR1YWwgLS0-fHl8d3JpdGVfMlsvV3JpdGUgd2F2L11cbiAgcGVyYy0tPnx5fHdyaXRlXzFbL1dyaXRlIHdhdi9dXG4gICIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggTFJcbiAgbG9hZC0tPnx5fHJlc2lkdWFsW3kgLSB4XVxuICBsb2FkWy9Mb2FkIHdhdi9dIC0tPnx5fGhhcm1vbmljW2hhcm1vbmljXVxuICBoYXJtb25pYy0tPnx5fHdyaXRlXzBbL1dyaXRlIHdhdi9dXG5cbiAgaGFybW9uaWMgLS0-fHl8YWRkW3kgKyB4XVxuICBsb2FkIC0tPnx5fHBlcmNbcGVyY3Vzc2l2ZV1cbiAgcGVyYyAtLT58eHxhZGRbeSArIHhdXG4gIGFkZCAtLT4gfHh8cmVzaWR1YWxcbiAgcmVzaWR1YWwgLS0-fHl8d3JpdGVfMlsvV3JpdGUgd2F2L11cbiAgcGVyYy0tPnx5fHdyaXRlXzFbL1dyaXRlIHdhdi9dXG4gICIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)


```mermaid
graph LR
  load-->|y|residual[y - x]
  load[/Load wav/] -->|y|harmonic[harmonic]
  harmonic-->|y|write_0[/Write wav/]

  harmonic -->|y|add[y + x]
  load -->|y|perc[percussive]
  perc -->|x|add[y + x]
  add --> |x|residual
  residual -->|y|write_2[/Write wav/]
  perc-->|y|write_1[/Write wav/]
```


## `master`

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbmxvYWQtLT58eXxhZGRfcmF3Mlt5ICsgeF1cbiAgbG9hZC0tPnx5fHJlc2lkdWFsW3kgLSB4XVxuICBsb2FkIC0tPnx5fHBlcmNbcGVyY3Vzc2l2ZV1cbiAgbG9hZFsvTG9hZCB3YXYvXSAtLT58eXxoYXJtb25pY1toYXJtb25pY11cbiAgbG9hZC0tPnx5fGFkZF9yYXdbeSArIHhdXG4gIGdyaWZmaW5saW1fMS0tPnx4fGFkZF9yYXcyXG4gIGFkZF9yYXctLT5tZXJnZXJbQ2hhbm5lbCBtZXJnZXJdXG4gIGFkZF9yYXcyLS0-bWVyZ2VyW0NoYW5uZWwgbWVyZ2VyXVxuICBncmlmZmlubGltXzItLT58eHxhZGRfcmF3XG4gIGhhcm1vbmljIC0tPnx4fGFkZFt5ICsgeF1cbiAgaGFybW9uaWMtLT58eXxzdGZ0XzJbc3RmdF1cbiAgc3RmdF8yLS0-fFN8emVyb3NfaHAyW1plcm8gPiBmbWluXVxuICBwZXJjIC0tPnx5fGFkZFt5ICsgeF1cbiAgYWRkIC0tPiB8eHxyZXNpZHVhbFxuICByZXNpZHVhbCAtLT58eXxzdGZ0XzFbc3RmdF1cbiAgemVyb3NfaHAtLT58U3xncmlmZmlubGltXzFbZ3JpZmZpbmxpbV1cbiAgemVyb3NfaHAyLS0-fFN8Z3JpZmZpbmxpbV8yW2dyaWZmaW5saW1dXG4gIHN0ZnRfMS0tPnxTfHplcm9zX2hwW1plcm8gPiBmbWluXVxuICBtZXJnZXItLT58eXx3cml0ZVtXcml0ZSB3YXZdIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggTFJcbmxvYWQtLT58eXxhZGRfcmF3Mlt5ICsgeF1cbiAgbG9hZC0tPnx5fHJlc2lkdWFsW3kgLSB4XVxuICBsb2FkIC0tPnx5fHBlcmNbcGVyY3Vzc2l2ZV1cbiAgbG9hZFsvTG9hZCB3YXYvXSAtLT58eXxoYXJtb25pY1toYXJtb25pY11cbiAgbG9hZC0tPnx5fGFkZF9yYXdbeSArIHhdXG4gIGdyaWZmaW5saW1fMS0tPnx4fGFkZF9yYXcyXG4gIGFkZF9yYXctLT5tZXJnZXJbQ2hhbm5lbCBtZXJnZXJdXG4gIGFkZF9yYXcyLS0-bWVyZ2VyW0NoYW5uZWwgbWVyZ2VyXVxuICBncmlmZmlubGltXzItLT58eHxhZGRfcmF3XG4gIGhhcm1vbmljIC0tPnx4fGFkZFt5ICsgeF1cbiAgaGFybW9uaWMtLT58eXxzdGZ0XzJbc3RmdF1cbiAgc3RmdF8yLS0-fFN8emVyb3NfaHAyW1plcm8gPiBmbWluXVxuICBwZXJjIC0tPnx5fGFkZFt5ICsgeF1cbiAgYWRkIC0tPiB8eHxyZXNpZHVhbFxuICByZXNpZHVhbCAtLT58eXxzdGZ0XzFbc3RmdF1cbiAgemVyb3NfaHAtLT58U3xncmlmZmlubGltXzFbZ3JpZmZpbmxpbV1cbiAgemVyb3NfaHAyLS0-fFN8Z3JpZmZpbmxpbV8yW2dyaWZmaW5saW1dXG4gIHN0ZnRfMS0tPnxTfHplcm9zX2hwW1plcm8gPiBmbWluXVxuICBtZXJnZXItLT58eXx3cml0ZVtXcml0ZSB3YXZdIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)

```mermaid
graph LR
load-->|y|add_raw2[y + x]
  load-->|y|residual[y - x]
  load -->|y|perc[percussive]
  load[/Load wav/] -->|y|harmonic[harmonic]
  load-->|y|add_raw[y + x]
  griffinlim_1-->|x|add_raw2
  add_raw-->merger[Channel merger]
  add_raw2-->merger[Channel merger]
  griffinlim_2-->|x|add_raw
  harmonic -->|x|add[y + x]
  harmonic-->|y|stft_2[stft]
  stft_2-->|S|zeros_hp2[Zero > fmin]
  perc -->|y|add[y + x]
  add --> |x|residual
  residual -->|y|stft_1[stft]
  zeros_hp-->|S|griffinlim_1[griffinlim]
  zeros_hp2-->|S|griffinlim_2[griffinlim]
  stft_1-->|S|zeros_hp[Zero > fmin]
  merger-->|y|write[Write wav]
```
