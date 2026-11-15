# AI Visibility Checklist

A practical audit checklist for making a site easier for answer engines and AI search to access and understand.

## Read this first

AI search systems do not publish ranking or citation rules. No item below is a guarantee of being cited, quoted or recommended by ChatGPT, Perplexity, Gemini, Google AI Overviews or any other system. Items are labelled honestly:

- **Verified guidance**: stated in official documentation from a search engine or the crawler's operator.
- **Good practice**: widely accepted for usability and classic SEO, but not documented as an AI citation factor.
- **Hypothesis**: plausible and cheap to try, with no solid evidence. Test it, do not assume it.

Official docs change. Re-check the source before relying on a label, especially for crawler names.

---

## 1. Crawl access

Blocking or allowing AI crawlers is a business decision (content licensing, bandwidth, brand exposure, traffic expectations). There is no single right answer.

- [ ] Open `https://yourdomain/robots.txt` and read it. Confirm it loads with HTTP 200 and has no accidental `Disallow: /`. *Verified guidance (Google Search Central robots.txt docs).*
- [ ] Decide deliberately about each of these robots.txt user agents: `GPTBot` (OpenAI training crawler), `ClaudeBot` (Anthropic), `PerplexityBot` (Perplexity search index), `Google-Extended` (Google control token for use of content by Gemini models and grounding; it does not change Google Search inclusion or ranking). *Verified guidance (each operator's own documentation).*
- [ ] Note that some vendors use separate agents for training versus search or user-initiated fetching (for example OpenAI documents `OAI-SearchBot` and `ChatGPT-User` separately from `GPTBot`). Blocking one does not block the others. *Verified guidance (operator documentation).*
- [ ] Remember robots.txt is a voluntary standard. It does not enforce access. Use authentication or server rules for content that must be private. *Verified guidance.*
- [ ] Make sure key pages are not blocked by `noindex`, login walls or heavy client-side rendering. *Verified guidance for Google; good practice for other systems.*
- [ ] Publish an XML sitemap and reference it in robots.txt. *Verified guidance.*
- [ ] Optional: publish `/llms.txt` (see `llms_txt_generator.py`). It is a proposal, major providers have not committed to using it. *Hypothesis.*

## 2. Page structure

- [ ] One clear H1 that matches the page topic, with a logical H2/H3 hierarchy. *Good practice.*
- [ ] Answer-first writing: state the direct answer in the first one or two sentences under a heading, then add detail. *Good practice (and a hypothesis that it helps extraction).*
- [ ] Phrase some headings as the questions people actually ask. *Good practice.*
- [ ] Give concise definitions of key terms in plain sentences, not only in images or PDFs. *Good practice.*
- [ ] Add an FAQ section for real recurring questions, visible on the page. *Good practice.*
- [ ] Use real HTML tables for comparisons, specifications and pricing rather than images. *Good practice.*
- [ ] Keep essential content in HTML text, not only in images, video or scripts. *Verified guidance (Google: make content available as text).*
- [ ] Google states there are no extra technical requirements to appear in AI features such as AI Overviews beyond being indexed and eligible for snippets, and that normal SEO best practices apply. *Verified guidance (Google Search Central).*

## 3. Entity clarity

Help machines and people tell who you are and what you offer.

- [ ] Use one consistent business or brand name (and address and phone where relevant) across your site and public profiles. *Good practice.*
- [ ] Have an About page stating who runs the business, what it does, where it operates and how to contact it. *Good practice.*
- [ ] Show real authors with bios on editorial content. *Good practice (aligns with Google's people-first content guidance).*
- [ ] Link to your official profiles with `sameAs` in Organization markup (see `schema_templates.md`). *Good practice.*
- [ ] Keep third-party listings (Google Business Profile, directories, social profiles) consistent with the site. *Good practice.*
- [ ] Hypothesis: consistent naming across the web makes it easier for AI systems to attribute facts to the right entity. *Hypothesis.*

## 4. Structured data

- [ ] Add JSON-LD that matches visible content: Organization, WebSite, and page-specific types such as Product, Article, FAQPage or LocalBusiness. *Verified guidance (Google structured data guidelines).*
- [ ] Do not mark up content that users cannot see. *Verified guidance.*
- [ ] Validate with the Rich Results Test and the Schema.org validator, and fix errors and warnings. *Verified guidance (tooling documented by Google).*
- [ ] Monitor structured data reports in Google Search Console. *Verified guidance.*
- [ ] Hypothesis: clean structured data may help non-Google AI systems parse facts such as price or authorship. No provider has documented this. *Hypothesis.*

## 5. Freshness

- [ ] Show a visible published or updated date on time-sensitive content, and make it match `datePublished` and `dateModified` in markup. *Verified guidance (Google date guidelines).*
- [ ] Only change the modified date when the content really changed. *Verified guidance.*
- [ ] Keep `lastmod` in your sitemap accurate. *Verified guidance (Google sitemap docs).*
- [ ] Review pricing, policies, specs and statistics on a schedule and remove outdated claims. *Good practice.*

## 6. Measurement

You cannot read AI ranking positions, so measure with a repeatable manual process.

- [ ] Write 15 to 30 realistic prompts a customer might ask (category questions, comparison questions, "best X for Y", brand questions). *Good practice.*
- [ ] Run them on a fixed schedule (for example monthly) in each system you care about, using a logged-out or clean session where possible, because answers vary by session, location and time. *Good practice.*
- [ ] Log each run in a spreadsheet: date, system, prompt, whether your brand appeared, whether your URL was cited, which competitors appeared, and whether the facts stated were correct. *Good practice.*
- [ ] Repeat each prompt a few times; outputs are non-deterministic, so one result proves little. *Good practice.*
- [ ] Review server logs for the crawler user agents above to confirm what actually visits. User agents can be spoofed, so verify with the operator's published IP ranges where available. *Good practice.*
- [ ] In analytics, segment referral traffic from known AI products and track it separately. Attribution is incomplete, so treat numbers as indicative. *Good practice.*
- [ ] Change one thing at a time and record the date, so you can compare later. Do not claim cause and effect from a small sample. *Good practice.*
