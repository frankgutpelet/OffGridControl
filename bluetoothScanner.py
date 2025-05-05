import asyncio
from bleak import BleakScanner


async def main():
    print("Suche nach BLE-Geräten...")

    # Erstelle ein Dictionary, um die gefundenen Geräte zu speichern
    allDevices = {}

    # Schleife, um mehrfach zu scannen (z. B. 10 Scans durchführen)
    for i in range(1, 100):
        print(".")
        devices = await BleakScanner.discover()
        for d in devices:
            # Füge Geräte zu allDevices hinzu (nur wenn sie noch nicht vorhanden sind)
            if d.address not in allDevices:
                allDevices[d.address] = (
                d.name, d.address, d.rssi, d.metadata.get('is_connectable'), d.metadata.get('manufacturer_data'),
                d.metadata.get('uuids'))
                print( d.name + "," + str(d.address) + "," + str(d.rssi) + "," + str(d.metadata.get('manufacturer_data')) + "," + str(d.metadata.get('uuids')))



# Starte den asynchronen Code
asyncio.run(main())
