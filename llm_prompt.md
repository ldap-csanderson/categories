# Website Taxonomy Generation System

You will generate a hierarchical taxonomy of products, services, and offerings for a given website, using both your general knowledge and provided content for validation. The output should capture categories suitable for advertising purposes.

# Input
- URL: The website's main URL
- Content: Scraped textual content from the website

# Analysis Approach

## First Pass - General Knowledge
1. Consider your existing knowledge about:
   - The website/company's main offerings
   - The industry's standard categorization patterns
   - Typical product/service hierarchy for this business type
   - Known major categories and subcategories

2. Structure initial taxonomy based on:
   - Main product/service lines
   - Target audiences
   - Delivery methods
   - Industry-standard groupings

## Second Pass - Content Validation
1. Compare your knowledge against scraped content:
   - Confirm existing categories
   - Identify new offerings
   - Remove deprecated categories
   - Update terminology
   - Validate hierarchy

2. Look for structural clues in:
   - Navigation menus
   - URL patterns
   - Page headers
   - Product groupings
   - Section organization

# Output Format
Generate a CSV file with the following columns:
1. taxonomy: The hierarchical category path (e.g., "Category > Subcategory")
2. seasonal: Boolean (TRUE/FALSE) indicating if this is a seasonal offering
3. confidence: Rating of classification confidence (weak/moderate/strong)
4. source_url: URL where this category was identified
5. date_scraped: Date when the content was scraped
6. reasoning: Explanation of categorization decision

Example header row:
```
"taxonomy","seasonal","confidence","source_url","date_scraped","reasoning"
```

# CSV Formatting Rules
1. Each field MUST be enclosed in double quotes
2. Internal double quotes must be escaped by doubling them
3. Use comma as delimiter between fields (not within fields)
4. Each value must be in its own field - never combine multiple values in one field
5. Use YYYY-MM-DD date format
6. Use uppercase TRUE/FALSE for seasonal (as separate field)
7. Use lowercase weak/moderate/strong for confidence (as separate field)

## Good Examples:
```csv
"taxonomy","seasonal","confidence","source_url","date_scraped","reasoning"
"Learning Programs > Degrees > Master's Degrees","FALSE","strong","coursera.org/degrees","2024-12-05","Known offering confirmed in main navigation"
"Subject Areas > Business","FALSE","strong","coursera.org/browse/business","2024-12-05","Major category confirmed in navigation"
```

## Bad Examples (Do Not Generate):
```csv
"Learning Programs > Degrees","FALSE,strong","coursera.org"         // Combined values in one field
"Subject Areas > Business","FALSE, moderate","coursera.org"         // Space after comma, still combined
"Learning Programs","FALSE,","coursera.org"                         // Trailing comma
"Subject Areas",FALSE,"moderate","coursera.org"                     // Missing quotes around boolean
```

## Field-Specific Rules:
1. taxonomy: 
   - Double-quoted string
   - Use ">" as hierarchy separator
   - Example: "Category > Subcategory > Item"

2. seasonal:
   - Must be exactly "TRUE" or "FALSE"
   - Always double-quoted
   - Example: "FALSE"

3. confidence:
   - Must be exactly "weak", "moderate", or "strong"
   - Always double-quoted
   - Example: "moderate"

4. source_url:
   - Double-quoted string
   - Full URL
   - Example: "https://example.com/page"

5. date_scraped:
   - YYYY-MM-DD format
   - Double-quoted
   - Example: "2024-12-05"

6. reasoning:
   - Double-quoted string
   - Escape any internal quotes
   - Example: "Found in ""About Us"" section"

## Confidence Rating Definitions:
- strong: 
  * Exists in your knowledge AND confirmed in scraped content
  * OR Multiple strong signals in scraped content
- moderate:
  * Exists in your knowledge but partially/indirectly confirmed in content
  * OR Clear evidence in scraped content alone
- weak:
  * Exists in your knowledge but not found in scraped content
  * OR Inferred from limited content signals

# Taxonomy Rules

## Hierarchy Guidelines
1. Always create full paths from highest level to specific offering
2. Minimum 2 levels for most items
3. Maximum 9 levels deep
4. Create parallel structures for similar items
5. Group related items consistently

## Common Hierarchy Patterns
1. Product Type > Specific Product
2. Subject Area > Specific Subject
3. Solution Type > Target Audience
4. Format > Delivery Method

## Naming Conventions
1. Start all categories with nouns
2. Use Title Case for all words except articles and prepositions
3. Use only industry-standard abbreviations (e.g., B2B, SaaS)
4. No special characters except ">" for hierarchy
5. Be consistent across similar categories

# Examples

## Processing Example (Coursera)

1. General Knowledge Analysis:
```
Known offerings:
- Online degrees (Bachelor's, Master's)
- Professional certificates
- Individual courses
- Enterprise solutions
- Subject areas (Business, Computer Science, etc.)
```

2. Content Validation:
```
Confirmed in content:
- Degree programs still current
- Professional certificates active
- Enterprise solution branded as "Coursera for Business"
- New offering: Career Academy
```

3. Final Output:
```
"Learning Programs > Degrees > Master's Degrees","FALSE","strong","coursera.org/degrees","2024-12-05","Known offering confirmed in main navigation and degree catalog"
"Learning Programs > Degrees > Bachelor's Degrees","FALSE","strong","coursera.org/degrees","2024-12-05","Known offering validated by degree pages"
"Learning Programs > Certificates > Professional Certificates","FALSE","strong","coursera.org/certificates","2024-12-05","Confirmed in both knowledge base and current content"
"Professional Development > Career Academy","FALSE","moderate","coursera.org/academy","2024-12-05","New offering found in current content, not in prior knowledge"
"Subject Areas > Business","FALSE","strong","coursera.org/browse/business","2024-12-05","Major category confirmed in navigation and content"
"Enterprise Solutions > Coursera for Business","FALSE","strong","coursera.org/business","2024-12-05","Known offering with updated branding from content"
```

## Bad Examples (Do Not Generate)
```
"Website > Navigation > Top Menu"  // Describes structure, not offerings
"Products > Things > Items"        // Too vague
"Services > Misc > Other"         // Not specific enough
"Master's Degrees"                // Missing parent categories
"Business"                        // Too broad, needs full path
```

# Special Cases

## Unknown Website Handling
- If you don't recognize the website, note this in reasoning and rely on content
- If website appears to be different from your knowledge (e.g., different company with same name), use content-only analysis

## Content Discrepancy Handling
- When content contradicts knowledge, prefer recent content
- Document significant changes in reasoning column
- Use weak confidence for removed/deprecated categories

## Edge Cases
- Return "<none>" for empty websites
- Return "<unknown>" for unclear structure
- Mark seasonal items TRUE but include in main taxonomy
- Create separate entries for items fitting multiple categories

# Quality Checklist
1. All major categories identified
2. Proper hierarchy depth
3. Consistent naming
4. Complete paths
5. Appropriate confidence ratings
6. Clear reasoning provided
7. Proper CSV formatting
8. Every field properly quoted
9. No combined values in single fields
10. Consistent delimiter usage
11. Proper value formatting for each field type

The final output must strictly follow CSV formatting rules to ensure reliable automated processing. The final output should be both human-readable and suitable for automated processing, with each row representing a distinct advertising-targetable category or subcategory.
