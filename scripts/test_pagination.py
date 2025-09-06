import asyncio
# 1. Import the 'engine' from your connection manager
from core.database.connection_manager import engine
from core.mcp.tools.get_table_data import run_get_table_data

# --- Make sure this is your table name ---
TABLE_TO_TEST = 'employees'
# ----------------------------------------

async def main():
    """
    An async function to run our pagination test and ensure graceful shutdown.
    """
    try:
        print(f"--- Testing Pagination for table: '{TABLE_TO_TEST}' ---")
        
        # Test Case 1: Fetch the first page with 5 items
        print("\n[TEST 1] Fetching Page 1 (5 items per page)...")
        page_1_result = await run_get_table_data(
            table_name=TABLE_TO_TEST,
            page=1,
            page_size=5
        )
        print("Response for Page 1:")
        print(page_1_result)
        
        # Test Case 2: Fetch the second page with 5 items
        print("\n[TEST 2] Fetching Page 2 (5 items per page)...")
        page_2_result = await run_get_table_data(
            table_name=TABLE_TO_TEST,
            page=2,
            page_size=5
        )
        print("Response for Page 2:")
        print(page_2_result)

        # Verify that the data is different for each page
        if page_1_result['status'] == 'success' and page_2_result['status'] == 'success':
            if page_1_result.get('data') and page_1_result['data'] != page_2_result.get('data'):
                print("\n✅ SUCCESS: The data for Page 1 and Page 2 is different, as expected.")
            else:
                print("\n⚠️  NOTICE: The data for Page 1 and 2 is the same. This can happen if your table has 10 or fewer rows.")
        else:
            print("\n❌ ERROR: One of the test cases failed. Check the error messages above.")

    finally:
        # 2. This block will run after the tests, closing the connection pool gracefully
        print("\nShutting down database connection pool...")
        await engine.dispose()
        print("Shutdown complete.")


if __name__ == "__main__":
    # This runs the async main function
    asyncio.run(main())