
import csv

class CsvExportPipeline:
    def open_spider(self, spider):
        self.file = open(f"{spider.name}.csv", "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["id", "mpn", "ean", "url", "name", "description",
                              "average_rating", "reviews_amount", "price", "stock"])

    def close_spider(self):
        self.file.close()

    def process_item(self, item):
        self.writer.writerow([
            item.get("id"),
            item.get("mpn"),
            item.get("ean"),
            item.get("url"),
            item.get("name"),
            item.get("description"),
            item.get("average_rating"),
            item.get("reviews_amount"),
            item.get("price"),
            item.get("stock")
        ])
        return item
