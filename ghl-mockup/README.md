# GHL My-Links Page Mockup

This folder contains the mockup for the `/my-links` page that goes on each client's website in GHL.

## What This Page Does

Gives clients a single place to find their important links:
- Their website URL
- Their Google review link
- Their business phone number
- App download links
- Help center link

## How to Add to Main Snapshot Template

### Step 1: Create the Page

1. Go to **Main Snapshot** sub-account in GHL
2. Navigate to **Sites** → **[Client Website]**
3. Click **+ Add New Page**
4. Name it: `My Links` or `Quick Links`
5. Set URL path: `/my-links`

### Step 2: Build the Page Structure

Create these sections (top to bottom):

#### Header Section
- Background: White or light gray
- Centered text
- Headline: `Welcome Back!`
- Subheadline: `Here are your important links, {{custom_values.company_name}}`

#### Link Cards (4 cards)

**Card 1: Your Website**
- Icon: 🌐 or globe icon
- Label: YOUR WEBSITE
- Value: `{{custom_values.company_website_link}}`
- Note: "Share this with customers, add to business cards, use in emails."
- Button: "Visit Your Website" → links to `{{custom_values.company_website_link}}`

**Card 2: Your Review Link**
- Icon: ⭐ or star icon
- Label: YOUR REVIEW LINK
- Value: `{{custom_values.review_google_url}}`
- Note: "Send this to happy customers. They'll be taken directly to leave a Google review."
- Button: "Test Review Link" → links to `{{custom_values.review_google_url}}`

**Card 3: Your Business Phone**
- Icon: 📞 or phone icon
- Label: YOUR BUSINESS PHONE
- Value: `{{custom_values.company_twilio_phone}}`
- Note: "This is your dedicated business line. Customers call this → rings your phone."
- Make phone number clickable: `tel:{{custom_values.company_twilio_phone}}`

**Card 4: Download the App**
- Icon: 📱 or mobile icon
- Label: DOWNLOAD THE APP
- Note: "Your command center for leads, messages, and reviews."
- Two buttons side by side:
  - iPhone → App Store link
  - Android → Google Play link

#### Help Section
- Background: White card
- Centered text
- Headline: `Need Help?`
- Text: "Visit our help center or contact support:"
- Link: `help.slatesystems.io`
- Contact info: Text number + email

#### Footer Note
- Simple text: "Bookmark this page — come back anytime you need your links!"

### Step 3: Styling

Match the client site styling:
- Use same fonts (probably Montserrat)
- Use client's primary/secondary colors for buttons
- Cards: white background, slight shadow, rounded corners
- Keep it clean and simple

### Step 4: Test Custom Values

Before saving, verify these custom values exist in Settings → Custom Values:
- `company_name` ✓
- `company_website_link` ✓
- `review_google_url` ✓
- `company_twilio_phone` ✓

If any are missing, add them with placeholder values.

### Step 5: Save to Snapshot

Once built in Main Snapshot:
1. Save the page
2. Update the Main Snapshot
3. Every new client will get this page automatically

## Custom Values Reference

| Custom Value | What It Is | Example |
|--------------|------------|---------|
| `{{custom_values.company_name}}` | Business name | Sergeant Painters |
| `{{custom_values.company_website_link}}` | Full website URL | https://www.sergeantpainters.com |
| `{{custom_values.review_google_url}}` | Direct Google review link | https://g.page/r/xxx/review |
| `{{custom_values.company_twilio_phone}}` | Business number | (800) 123-4567 |

## Visual Reference

Open `my-links.html` in a browser to see how it should look. This is a mockup — copy the DESIGN into GHL, not the HTML code.

## Page Settings

- **Page Title:** Your Quick Links
- **URL Path:** /my-links
- **Visibility:** Published
- **Show in Navigation:** No (clients access via direct link)

## How Clients Find This Page

1. Launch call: "Bookmark yoursite.com/my-links for your links"
2. Post-launch SMS: Include the link
3. Help website: References "yoursite.com/my-links" for personalized links
