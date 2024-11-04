import csv
import os

class FileReader:
    """
    The FileReader class is responsible for reading CSV files and returning data
    as a list of dictionaries, where each dictionary represents a row in the CSV file.
    """
    @staticmethod
    def read_csv(file_path):
        if not os.path.exists(file_path):
            print(f"File {file_path} not found.")
            return []

        try:
            with open(file_path, newline='', encoding='utf-8') as file:
                return list(csv.DictReader(file))
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

class ItemManager:
    """
    The ItemManager class manages item data: loading, searching by ID, and by name.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.items = []

    def load_items(self):
        self.items = FileReader.read_csv(self.file_path)

    def get_items_by_id(self, item_id):
        return [item for item in self.items if item['ID'] == str(item_id)]

    def search_by_name(self, name):
        return [item for item in self.items if name.lower() in item['Name'].lower()]

class CSVSurvivorItems:
    """
    Class for working with survivor items from a CSV file.
    """
    def __init__(self, file_path):
        self.item_manager = ItemManager(file_path)
        self.item_manager.load_items()

    def display_items(self, page_size=10, page_number=1, filter_by=None, filter_value=None):
        items_to_display = self.item_manager.items

        # Apply filtering if criteria are provided
        if filter_by and filter_value:
            items_to_display = [
                item for item in items_to_display
                if str(item.get(filter_by, "")).lower() == str(filter_value).lower()
            ]

        # Sort by ID for convenience
        items_to_display.sort(key=lambda x: int(x['ID']))

        # Pagination
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        items_to_display = items_to_display[start_index:end_index]

        # Display table
        if items_to_display:
            column_widths = {'ID': 5, 'Name': 20, 'Type': 15, 'Condition': 10, 'Amount': 7}
            header = f"{'ID'.ljust(column_widths['ID'])} | {'Name'.ljust(column_widths['Name'])} | {'Type'.ljust(column_widths['Type'])} | {'Condition'.ljust(column_widths['Condition'])} | {'Amount'.ljust(column_widths['Amount'])}"
            print(header)
            print('-' * len(header))

            for item in items_to_display:
                row = f"{item['ID'].ljust(column_widths['ID'])} | {item['Name'].ljust(column_widths['Name'])} | {item['Type'].ljust(column_widths['Type'])} | {item['Condition'].ljust(column_widths['Condition'])} | {item['Amount'].ljust(column_widths['Amount'])}"
                print(row)
        else:
            print("No items to display for the given criteria.")

# Testing code
if __name__ == "__main__":
    file_path = 'items.csv'
    csv_items = CSVSurvivorItems(file_path)

    # Display items by ID
    print("Filtering by ID:")
    csv_items.display_items(filter_by='ID', filter_value='2')

    # Display items by name
    print("\nFiltering by name:")
    csv_items.display_items(filter_by='Name', filter_value='Nails')

    # Paginated display of items
    print("\nPaginated display:")
    csv_items.display_items(page_size=10, page_number=1)
