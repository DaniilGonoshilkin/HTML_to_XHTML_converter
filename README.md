# HTML to XHTML converter

This script was designed to convert HTML tags to XHTML tags for compliance with SDL Tridion software used by our internal customer. I've tried to search for existing solutions to the initial problem but none of those were compatible with initial conditions so I decided to write my own converter.

## Problem

We use Smartcat (Cloud base CAT-tool) company-wide to perform translation tasks. Our internal customer asked us to translate multiple articles for our company's Knoledge Base website. Since the customer is using SDL Tridion software to publish articles, one of the requirements was to keep XHTML tags in translated files. However, the main problem here is that Smartcat ignores XHMTL tags when handling files, and generates resulting translations as HTML-compatible files only (all lowercase), which causes errors when reuploading them back to SDL Tridion. Here are some exapmles:
>
    <Title>Premium Support</Title> → <title>Поддръжка Premium</title>
    <ImageAltText>Premium Support</ImageAltText>→ <imagealttext>Поддръжка Premium</imagealttext>
    <Option>Remote diagnostics</Option>→ <option>Отдалечена диагностика</option>

## Solution

The Smartcat support said, that there are no plans to add XHTML support in near future, so I decided to design a script that 'restores' XHTML tags in translated files. The script uses Beautiful Soup package.

# General info

## File types

This script works with .html files only. If your .html file has XHTML-compatible tags and your CAT-tool converts it to HTML-only, this script might help you to convert your translations back to XHTML-compatible files.

## File specifications

In order for the script to work, you should have:
* source files (with XHTML tags, before translation)
* target files (generated from CAT-tool with HTML-only tags)

## How the script works

The script can work with multiple source files and also can work with multiple languages for target files. The script matches source file with its target translation, then parses both files with BeautifulSoup module to create a dictionary data type with matching lists of tags. Secondly, the script reads target file and replaces tags according to the created dictionary (as well as some other repalcements that couldn't be done initially).

## Languages

The script works with any language, since it only works with HTML tags and not the actual text.

## Results

The script allows to achive the following results:
* quickly restore initial XHTML-compatibility without significantly changing your current workflow

# How to use

## 1. Clone the repository:

    git clone https://github.com/DaniilGonoshilkin/HTML_to_XHTML_converter.git

## 2. Install dependencies: 

    pip install -r requirements.txt

## 3. Run the script

Run the following command in Console

      python html2xhtml.py `<PATH TO SOURCE FILES>` `<PATH TO TARGET FILES>` `<PATH TO PUT PROCESSED FILES>`
