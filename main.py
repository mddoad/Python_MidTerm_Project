from inventory_manager import InventoryManager
from storage import JsonStore 

def main():
    store = JsonStore("data/inventory.json")
    manager = InventoryManager()

    manager.load_from_dicts(store.load())

    if not manager.products:
        print("No products found. Adding sample products.")
        manager.add_product("Apple", 0.5, 100)
        manager.add_product("Banana", 0.3, 150)
        manager.add_product("Orange", 0.8, 80)
        store.save(manager.to_dicts())

        print("Products:", manager.to_dicts())
        print("Total inventory value:", manager.total_inventory_value())

if __name__ == "__main__":
    main()