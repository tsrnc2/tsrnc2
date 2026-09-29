# Jacob W. Wood

### C/C++ systems engineer (since 1999) building LLM-guided infrastructure

I design and own native Linux/POSIX systems in C++17/20, and I use LLM agents as a
supervised engineering workforce inside them. Agents propose, implement, and test.
The systems I architect decide what is allowed to ship: typed contracts, bounded
authority, human approval gates, signed artifacts, and fail-closed defaults.

- **Core:** C++17/20, C (POSIX, ISO C17), Python, Bash · CMake/Make · g++ & clang++ `-Werror`
- **Systems:** fork/exec, poll, flock, signals, sockets, threads/atomics · SQLite, libcurl, OpenSSL · static musl cross-builds (zig) · Qt6
- **LLM infrastructure:** supervisor loops over replaceable agents, provider routing (Ollama/qwen3, OpenRouter, LiteLLM, Claude Code, Codex CLI), quota/cost controls, eval harnesses, redacted tracing
- **Ops & embedded:** Docker Compose, systemd, WireGuard, MQTT, Home Assistant, ESPHome, Arch Linux, Termux/Android
- **Games:** Godot 3 → 4, C++ GDExtension (pathfinding, traffic simulation)

## Selected work

Most of my current work lives in private repositories. **Code walkthroughs are available on request.**

| Project | What it is | Stack | Visibility |
|---|---|---|---|
| **ckpatch** | Signed, git-native production patch pipeline. Each patch is an SSH-signed git bundle that goes through cached stages, a human approval bound to the artifact hash, deploy, verify, and auto-rollback. LLM repair loops are confined to declared writable roots. | C++20, POSIX, zig/musl | private, walkthroughs on request |
| **improved** | Supervisor-controlled agent patch orchestrator: replaceable proposal / test / eval / safety-review / decision agents behind governance gates and a sandboxed command boundary. Qt6 approval GUI. | C++17, Qt6 | private, walkthroughs on request |
| **kitt** | Multi-provider LLM delegator: provider registry and probes, quota broker, cost firewall, plugin API with capability policy, boundary tests, CI. (Routes to existing models; no custom model training.) | Python, Android | private, walkthroughs on request |
| **librem5-ha-stack** | C++ TUI/daemon that runs a Home Assistant / MQTT / Grafana / WireGuard / local-LLM Docker Compose stack, with systemd units and packaging. | C++, Bash, Compose | private, walkthroughs on request |
| **Native C++ trading-research engine** | Backtesting and strategy-tournament research platform. Research, dry-run, and paper trading only. | C++20, Python | private, walkthroughs on request |
| [**Traveler**](https://github.com/tsrnc2/Traveler) | Godot game about a train-hopping vagrant, with custom GLSL shaders. | GDScript, GLSL | public |

## How I work

Tiny, stable cores · typed contracts between components · bounded authority for every
agent · approval gates bound to hashes · reproducible builds with provenance ·
adversarial review before anything touches production.

Much of this code was written by AI coding agents working under my direction. I own
the architecture, the constraints, the review, and the result, and I'm happy to walk
through any design decision in detail.

Forks on this profile are upstream projects I've studied or experimented with. They
are not my original work.

---

Portland, OR · open to remote · contact details on my résumé
