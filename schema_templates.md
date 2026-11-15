# JSON-LD Schema Templates

Copy-paste templates for common schema.org types. Replace every value written as `REPLACE_...` before publishing. Delete optional properties you cannot fill honestly.

Rules that apply to every template:

1. Markup must match the visible content of the page. Do not mark up reviews, prices, FAQs or addresses that users cannot see on the page. Google's structured data guidelines say this explicitly (verified guidance).
2. Put each block in `<script type="application/ld+json">` in the `<head>` or `<body>`.
3. Validate with the Schema.org validator (https://validator.schema.org) and Google's Rich Results Test (https://search.google.com/test/rich-results). Valid markup does not guarantee rich results, and no schema type is documented to make AI systems cite a page.
4. Use absolute URLs, ISO 8601 dates (`2026-01-31`) and plain text with no HTML in string values.

---

## 1. Organization

Use on the home page or about page, once per site, to state who runs the site.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://REPLACE_DOMAIN/#organization",
  "name": "REPLACE_LEGAL_OR_BRAND_NAME",
  "url": "https://REPLACE_DOMAIN/",
  "logo": "https://REPLACE_DOMAIN/REPLACE_LOGO.png",
  "description": "REPLACE_ONE_SENTENCE_DESCRIPTION",
  "email": "REPLACE_PUBLIC_EMAIL",
  "sameAs": [
    "https://www.linkedin.com/company/REPLACE",
    "https://x.com/REPLACE",
    "https://www.youtube.com/@REPLACE"
  ]
}
</script>
```

Keep `sameAs` to profiles you actually own and that use the same name.

---

## 2. WebSite

Use on the home page to name the site. Add a `potentialAction` search box only if your site has a working search URL.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "https://REPLACE_DOMAIN/#website",
  "url": "https://REPLACE_DOMAIN/",
  "name": "REPLACE_SITE_NAME",
  "inLanguage": "en",
  "publisher": { "@id": "https://REPLACE_DOMAIN/#organization" }
}
</script>
```

---

## 3. FAQPage

Use only on a page that visibly shows these exact questions and answers. Google restricts FAQ rich results to a small set of sites, so treat this as clarity markup, not a way to get rich results.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "REPLACE_QUESTION_1",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "REPLACE_ANSWER_1_PLAIN_TEXT"
      }
    },
    {
      "@type": "Question",
      "name": "REPLACE_QUESTION_2",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "REPLACE_ANSWER_2_PLAIN_TEXT"
      }
    }
  ]
}
</script>
```

---

## 4. Product (with offers)

Use on a single product page. Price, currency and availability must match what the page shows. Add `aggregateRating` or `review` only if real, visible reviews exist on the page.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "REPLACE_PRODUCT_NAME",
  "description": "REPLACE_PRODUCT_DESCRIPTION",
  "sku": "REPLACE_SKU",
  "brand": { "@type": "Brand", "name": "REPLACE_BRAND" },
  "image": [
    "https://REPLACE_DOMAIN/REPLACE_IMAGE_1.jpg"
  ],
  "offers": {
    "@type": "Offer",
    "url": "https://REPLACE_DOMAIN/products/REPLACE_HANDLE",
    "priceCurrency": "USD",
    "price": "REPLACE_PRICE_E_G_49.00",
    "priceValidUntil": "REPLACE_YYYY-MM-DD",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  }
}
</script>
```

On Shopify, generate this from Liquid (product and variant objects) rather than hard-coding values, so price and stock stay in sync.

---

## 5. LocalBusiness

Use on the page for a business with a physical location or service area. Use a more specific subtype if one fits (for example `Dentist` or `Restaurant`). The address and hours must be visible on the page.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://REPLACE_DOMAIN/#localbusiness",
  "name": "REPLACE_BUSINESS_NAME",
  "url": "https://REPLACE_DOMAIN/",
  "telephone": "REPLACE_+COUNTRYCODE_NUMBER",
  "image": "https://REPLACE_DOMAIN/REPLACE_PHOTO.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "REPLACE_STREET",
    "addressLocality": "REPLACE_CITY",
    "addressRegion": "REPLACE_REGION",
    "postalCode": "REPLACE_POSTCODE",
    "addressCountry": "REPLACE_ISO_COUNTRY_CODE"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "sameAs": ["https://REPLACE_PROFILE_URL"]
}
</script>
```

---

## 6. Article

Use on a blog post or news article. The author, dates and headline must match the visible byline and content. Update `dateModified` only when the content genuinely changes.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "mainEntityOfPage": "https://REPLACE_DOMAIN/blog/REPLACE_SLUG",
  "headline": "REPLACE_HEADLINE_MATCHING_H1",
  "description": "REPLACE_SUMMARY",
  "image": ["https://REPLACE_DOMAIN/REPLACE_IMAGE.jpg"],
  "datePublished": "REPLACE_YYYY-MM-DD",
  "dateModified": "REPLACE_YYYY-MM-DD",
  "author": {
    "@type": "Person",
    "name": "REPLACE_AUTHOR_NAME",
    "url": "https://REPLACE_DOMAIN/authors/REPLACE_AUTHOR"
  },
  "publisher": { "@id": "https://REPLACE_DOMAIN/#organization" }
}
</script>
```
