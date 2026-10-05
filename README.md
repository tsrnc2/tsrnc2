# Jacob W. Wood

### Senior code review & team lead · I ship working, tested, secure software

**Shipped.** [Pity Please!](https://store.steampowered.com/app/1154140) has been live on Steam since Sep 2025. I directed the 6-person Godot/C++ team and owned its architecture and code review across 2,000+ commits, with Linux, Windows, and Android builds.

**Tested.** Tests ship with the code: unit, contract, golden, and security tests across my active repos, CI on those repos, and `-Werror` builds under both g++ and clang++.

**Secure.** Fail-closed defaults, sandboxed command boundaries, SSH-signed artifacts, approvals bound to artifact hashes, and redacted logs.

| Project | Proof |
|---|---|
| **ckpatch** (C++20) | Signed production patch pipeline. Every patch passes test, review, and human approval before it deploys, then gets verified with automatic rollback. |
| **improved** (C++17, ~35k LOC) | Supervised patch orchestrator with test, eval, safety-review, and decision gates, plus a Qt6 approval UI. |
| **Pity Please! GDExtension** (C++) | A* navmesh, behavior trees, and traffic sim, shipping in a commercial release. |
| [**Traveler**](https://github.com/tsrnc2/Traveler) | Public Godot 3 + GLSL project. |

I'm looking for **senior code-review and team-lead** roles, remote or Portland. Most repos are private, and I'm happy to do live walkthroughs. [LinkedIn](https://www.linkedin.com/in/jacobwwoodcpp/)

To be upfront: I haven't held a paid SWE title and I don't have a degree. AI agents write much of the implementation in my newer projects. I own the architecture, the tests, the review, and the call on what ships.
