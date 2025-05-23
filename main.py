import asyncio

# from secer import SecEdgerAsync


async def main():
    # print("Running SEC Edger....")

    # APPLE INC
    # await SecEdgerAsync(companyName="NFLX")
    print("PDF To Markdown...")


if __name__ == "__main__":
    asyncio.run(main())
# 10-K, 10-Q, 8-K, DEF 14A, F-4, S-1, SC 13D, SC 13G
# 10-K, 10-Q, 8-K, DEF 14A, F-4, S-1, SC 13D, SC 13G


# # Run multiple company searches concurrently
# async def main():
#     # More companies here
#     tasks = [
#         SecEdgerAsync("Apple Inc."),
#         SecEdgerAsync("Microsoft"),
#         SecEdgerAsync("Tesla"),
#         SecEdgerAsync("Google"),
#     ]
#     await asyncio.gather(*tasks)


# # Start the async event loop
# if __name__ == "__main__":
#     asyncio.run(main())


# -------------------------------------------------
# analysis/
# │
# ├── data/
# │   ├── raw/                  # Raw SEC filings (PDFs, XMLs, ZIPs)
# │   ├── processed/              # Processed JSON/Markdown output
# │   └── cache/                  # Temporary storage/cache for downloads
# │
# ├── src/
# │   ├── downloader.py           # Download filings by CIK/filing type from EDGAR
# │   ├── pdf_extractor.py        # Extract text/tables from PDFs
# │   ├── xbrl_parser.py          # Parse XBRL/XML financial statements
# │   ├── section_locator.py      # Locate named sections in text (e.g., Risk Factors)
# │   ├── formatter.py            # Format extracted data into Markdown/JSON
# │   ├── llm_interface.py        # Send formatted data to Qwen or other LLMs
# │   └── utils.py                # Helper functions (cleaning, logging, etc.)
# │
# ├── templates/
# │   └── markdown_template.md    # Template for final Markdown output
# │
# ├── models/
# │   └── (optional)              # ML/NLP models, embeddings, or cached LLM outputs
# │
# ├── tests/
# │   └── test_parsing.py         # Unit/integration tests for parsing logic
# │
# ├── config/
# │   └── settings.json           # API keys, default filing types, paths
# │
# ├── notebooks/
# │   └── analysis.ipynb          # Jupyter Notebook for interactive analysis/testing
# │
# ├── requirements.txt            # Python dependencies
# ├── README.md                   # Project overview
# └── run_pipeline.py             # Main script to run the full workflow
