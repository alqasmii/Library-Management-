/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

/**
 * Barcode Scanner Widget
 * Handles keyboard-wedge barcode scanner input for quick checkout/return
 */

class BarcodeScanner extends owl.Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.state = owl.useState({
            memberBarcode: "",
            bookBarcode: "",
            scanning: false,
        });
    }

    async processBarcodeScan(memberBarcode, bookBarcode) {
        try {
            const result = await this.orm.call(
                "library.barcode.scan",
                "create_and_process",
                [{
                    member_barcode: memberBarcode,
                    book_barcode: bookBarcode,
                    operation: "auto",
                }]
            );

            if (result.success) {
                this.notification.add(result.message, {
                    type: "success",
                    title: "Scan Successful",
                });
            } else {
                this.notification.add(result.message || "Scan failed", {
                    type: "danger",
                    title: "Scan Error",
                });
            }
        } catch (error) {
            this.notification.add(error.message || "An error occurred", {
                type: "danger",
                title: "Error",
            });
        }
    }
}

BarcodeScanner.template = "baramej_library_system.BarcodeScanner";

// Register the widget
registry.category("actions").add("library_barcode_scanner", BarcodeScanner);

export default BarcodeScanner;
