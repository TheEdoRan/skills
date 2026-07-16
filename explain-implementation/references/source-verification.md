# Source verification protocol

The point of this protocol: a citation is a promise that the link exists and
says what you claim. Recalled URLs break that promise silently. So the rule is
mechanical: **cite only what a tool call returned or confirmed in this
session.**

## Order of preference

1. **Context7 MCP** (`resolve-library-id` + `query-docs`) — best for library
   and framework APIs (React, Next.js, Prisma, ...). If the docs it returns
   include canonical URLs, those are verified. If it confirms the API but
   returns no URL, you may cite the official docs *site* by its well-known
   root (e.g. `https://react.dev`) plus the concept name, and mark deeper
   paths per rule 3 below.
2. **WebFetch / WebSearch** — for platform docs (MDN, PostgreSQL, RFCs, man
   pages), blog-level explanations of algorithms, or when Context7 lacks the
   library. A URL is verified when WebFetch returned its content, or when it
   appeared in WebSearch results you actually received. Prefer official
   documentation over blogs; a blog is acceptable for algorithmic/conceptual
   topics when no official doc exists.
3. **Fallback — no URL.** If neither tool can confirm a link (offline, tool
   unavailable, page not found): keep the explanation if it is valuable, and
   point to the source by name only — "see the PostgreSQL docs chapter on
   advisory locks". Never emit an unchecked URL, not even a plausible one,
   not even for famous pages. The exception is bare domain roots of major
   official docs (react.dev, developer.mozilla.org, postgresql.org) which may
   be cited without a fetch — deep paths may not.

## What needs a source

- Claims about what an API/hook/language feature does, its constraints, or
  its documented edge cases.
- Named algorithms and data structures (cite an authoritative explanation).
- "Little-known behavior" claims — these especially, since they are the most
  likely to be misremembered.

## What does NOT need an external source

- Repo-specific rationale: "this follows the existing pattern in
  `src/hooks/useAuth.ts`" — the code is the source; cite the path.
- Trivial, universally-known facts (what a for-loop does).
- The user's own requirements.

## Cost control

Verification runs once per cited concept, not per sentence. Batch the
lookups. If a lookup takes more than a couple of
attempts, fall back to rule 3 instead of burning the session's budget.
