---
layout: page
title: Private Inventory Guide
permalink: /private-inventory-guide/
---

# Private Inventory Guide

This guide explains how to link your own adventure PDFs (like those in your Google Drive) to this catalog so you can
open them directly.

## How it Works

The catalog can show a 📄 icon next to adventures you own. You provide a list (a "JSON" file) that matches the
adventure's ID to your private link.

**Privacy Note:** Your links are never shared with the public. Only people who have the URL to your inventory list can
see them, and only people you've authorized on Google Drive can actually open the files.

## Step 1: Create Your Inventory List

The easiest way to do this is using a Google Sheet or a simple text file.

### Option A: Google Drive (Best for Friends)

If you want to collaborate with friends, use Google Drive.

1. Create a JSON file (instructions below) and upload it to Google Drive.
2. Right-click the file > **Share**.
3. Add your friends' emails so they can see the file.
4. Set "General access" to **Anyone with the link** (this allows the catalog to read the list, but doesn't give them
   access to your PDFs unless you shared those too).
5. Use a [Direct Link Generator](https://sites.google.com/site/gdriveurlgenerator/) to get a "Raw" link to your file.

### Option B: GitHub Gist (Best for Individuals)

1. Go to [gist.github.com](https://gist.github.com/).
2. Paste your inventory data (see format below).
3. Click **Create secret gist**.
4. Click the **Raw** button to get the direct URL.
   *Note: Gists are usually owned by one person. For a group of friends to edit the same list, Google Drive is
   recommended.*

## The Data Format

Your file must look like this. The numbers are the "Product ID" from DMsGuild. You can [see an example file here]({{
site.baseurl }}/example_private_intentory.json).

```json
{
  "294570": "https://drive.google.com/file/d/1abc.../view",
  "520780": "https://drive.google.com/file/d/xyz.../view"
}
```

## Step 2: Connect to the Catalog

1. Open the [AL DC Catalog](https://hoshisabi.com/al_adventure_catalog/).
2. Click **Show Filters**.
3. Paste your URL into the **Private Inventory JSON URL** field and click **Apply**.
4. (Optional) Check the **Only show adventures in private inventory** box to hide anything you don't have a link for.

### Try the Example

If you want to see it in action, click the **Try Example** button in the filters panel.

* This will load a sample list of public Wizards of the Coast PDF previews.
* **Tip:** After clicking, select **"1 - Tyranny of Dragons"** in the Season filter. You will see green 📄 icons appear
  next to the titles—these represent your private links!

## Step 3: Sharing with Friends

Once you've set up your inventory, you can give your friends a "pre-loaded" link to the catalog. Just add
`?inventory=YOUR_URL` to the end of the website address:

`https://hoshisabi.com/al_adventure_catalog/?inventory=https://your-link-here.json`

When they click this, the catalog will automatically use your list!

---

## Advanced: Exporting from Google Sheets

If you have a large list in a Google Sheet, you can use this script to create your inventory file automatically while
keeping your links intact.

1. Open your Google Sheet (Column A = Product ID, Column B = Hyperlink).
2. Go to **Extensions > Apps Script**.
3. Paste this code and click **Run**:

```javascript
function exportToJson() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var data = sheet.getDataRange().getValues();
    var obj = {};
    for (var i = 1; i < data.length; i++) {
        var productId = String(data[i][0]).trim();
        var richValue = sheet.getRange(i + 1, 2).getRichTextValue();
        var url = richValue ? richValue.getLinkUrl() : null;
        if (!url) url = data[i][1];
        if (productId && url) obj[productId] = url;
    }
    var json = JSON.stringify(obj, null, 2);
    DriveApp.createFile('my_inventory.json', json, MimeType.PLAIN_TEXT);
    SpreadsheetApp.getUi().alert('Saved "my_inventory.json" to your Drive root!');
}
```
