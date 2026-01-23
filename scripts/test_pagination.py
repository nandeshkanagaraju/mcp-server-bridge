import asyncio
from core.database.connection_manager import engine
from core.mcp.tools.get_table_data import run_get_table_data

TABLE_TO_TEST = 'employees'

async def main():
    """
    An async function to run our pagination test and ensure graceful shutdown.
    """
    try:
        print(f"--- Testing Pagination for table: '{TABLE_TO_TEST}' ---")
        
        print("\n[TEST 1] Fetching Page 1 (5 items per page)...")
        page_1_result = await run_get_table_data(
            table_name=TABLE_TO_TEST,
            page=1,
            page_size=5
        )
        print("Response for Page 1:")
        print(page_1_result)
        
        print("\n[TEST 2] Fetching Page 2 (5 items per page)...")
        page_2_result = await run_get_table_data(
            table_name=TABLE_TO_TEST,
            page=2,
            page_size=5
        )
        print("Response for Page 2:")
        print(page_2_result)

        if page_1_result['status'] == 'success' and page_2_result['status'] == 'success':
            if page_1_result.get('data') and page_1_result['data'] != page_2_result.get('data'):
                print("\n✅ SUCCESS: The data for Page 1 and Page 2 is different, as expected.")
            else:
                print("\n⚠️  NOTICE: The data for Page 1 and 2 is the same. This can happen if your table has 10 or fewer rows.")
        else:
            print("\n❌ ERROR: One of the test cases failed. Check the error messages above.")

    finally:
        print("\nShutting down database connection pool...")
        await engine.dispose()
        print("Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())