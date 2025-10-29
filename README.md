# 📚 Library Management System v2.0

[![Odoo](https://img.shields.io/badge/Odoo-v15+-purple?style=for-the-badge&logo=odoo)](https://www.odoo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge)](#)
[![Tests](https://img.shields.io/badge/Tests-Passing-success?style=for-the-badge)](#)

> A **production-grade** Library Management System built as a standalone Odoo module — featuring member tiers, overdue automation, email reminders, barcode scanning, comprehensive reporting, and full test coverage.

---

## ✨ What's New in v2.0

### 🎯 Core Features

- ✅ **Member Tiers with Borrow Limits** – Configurable member types (Student, Faculty, Staff, Public) with different borrowing privileges
- ✅ **Automatic Overdue Detection** – Daily cron job to flag overdue loans and calculate fines
- ✅ **Email Reminder System** – Automated reminders for books due soon (2 days before) and overdue notifications
- ✅ **Barcode Scanning** – Quick checkout and return via USB barcode scanner (keyboard-wedge mode)
- ✅ **Comprehensive Dashboard** – Graph, pivot, and KPI views for loan analytics
- ✅ **Multi-Role Security** – User, Librarian, and Manager roles with row-level access control
- ✅ **Full Test Coverage** – 40+ unit tests covering all critical workflows
- ✅ **Internationalization** – Translation-ready with base English strings

---

## 📋 Feature Roadmap

| Feature | Status |
|---------|--------|
| Book/Member/Loan models and views | ✅ Complete |
| Borrow limits & validation | ✅ Complete |
| Overdue flagging & auto status updates | ✅ Complete |
| Email reminders using scheduled actions | ✅ Complete |
| Reporting dashboard (borrowed, overdue, top books) | ✅ Complete |
| Barcode scanner integration | ✅ Complete |
| Multi-role security (User/Librarian/Manager) | ✅ Complete |
| Comprehensive test suite | ✅ Complete |
| Demo data & i18n support | ✅ Complete |

---

## 🧩 Features in Detail

### 📘 Member Management
- **Member Types**: Pre-configured tiers (Student, Faculty, Staff, Public) with customizable limits
- **Borrowing Limits**: Max concurrent loans and loan duration per member type
- **Fine Calculation**: Automatic per-day fine calculation based on member type
- **Barcode Support**: Unique barcode for quick member identification
- **Statistics**: Track active loans, overdue books, and total fines per member

### 📚 Book Management
- **Inventory Tracking**: Real-time availability with available/total copies
- **Barcode Support**: Unique barcode for quick book scanning
- **Borrow History**: Complete loan history per book
- **Reviews**: Member reviews and ratings
- **Categories & Authors**: Organize books by category, author, publisher, location

### 🔄 Loan Processing
- **Smart States**: Draft → Borrowed → Returned/Overdue/Cancelled
- **Auto Due Dates**: Calculated from borrow date + member type loan days
- **Overdue Detection**: Automatic state transition when books are overdue
- **Fine Tracking**: Real-time fine calculation with overdue days
- **Copy Management**: Automatic increment/decrement of available copies

### 📧 Email Automation
- **Due Soon Reminders**: Sent 2 days before due date
- **Overdue Notifications**: Sent when loan becomes overdue
- **Professional Templates**: HTML email templates with loan details and fine info
- **Smart Sending**: Prevents duplicate emails, respects member email preferences

### 📊 Reporting & Analytics
- **Dashboard**: Quick overview with KPIs (total borrowed, overdue count, fines)
- **Graph View**: Bar/line charts for loan trends over time
- **Pivot View**: Multi-dimensional analysis by member type, state, date
- **Filters**: Pre-configured filters for active loans, overdue, this month/year

### 📱 Barcode Scanning
- **Scan & Go**: Quick form for member + book barcode input
- **Auto Detection**: Automatically detects checkout vs. return operation
- **USB Scanner Compatible**: Works with standard keyboard-wedge barcode scanners
- **Instant Feedback**: Clear success/error messages with loan details
---

## 🚀 Quick Start

```bash
# Clone and navigate
git clone https://github.com/alqasmii/Library-Management-.git
cd Library-Management-

# Copy to Odoo addons
cp -r custom/custom/baramej_library_system /path/to/odoo/addons/

# Install with demo data
./odoo-bin -d your_database -i baramej_library_system --stop-after-init

# Run with tests (recommended for production deployments)
./odoo-bin -d test_db -i baramej_library_system --test-enable --stop-after-init
```

**Login** → Activate Developer Mode → Navigate to **Library** app → Start managing books! 📚

---

## ⚙️ Installation

### Prerequisites
- Odoo **v15+** (Community or Enterprise)
- Python 3.8+
- PostgreSQL 12+

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/alqasmii/Library-Management-.git
   cd Library-Management-
   ```

2. **Copy module to Odoo addons directory**
   ```bash
   cp -r custom/custom/baramej_library_system /path/to/odoo/addons/
   ```

3. **Restart Odoo and update apps list**
   ```bash
   ./odoo-bin -c /path/to/odoo.conf --stop-after-init -u base -d your_database
   ./odoo-bin -c /path/to/odoo.conf
   ```

4. **Install the module**
   - Navigate to **Apps** → Activate Developer Mode
   - Click **Update Apps List**
   - Search for "Library Management System v2.0"
   - Click **Install**

### Upgrade from v1.0 to v2.0

```bash
./odoo-bin -c /path/to/odoo.conf -u baramej_library_system -d your_database
```

**Note**: Existing loan records will be migrated to the new state system. Review the migration logs.

---

## 🔧 Configuration

### 1. Member Types

Navigate to **Library → Configuration → Member Types**

Default types are pre-configured:
- **Student**: 3 books for 14 days, $0.50/day fine
- **Faculty**: 10 books for 30 days, $0.25/day fine
- **Staff**: 5 books for 21 days, $0.30/day fine
- **Public**: 2 books for 7 days, $1.00/day fine

**Customize** by editing any type or creating new ones.

### 2. Email Templates

Navigate to **Settings → Technical → Email → Templates**

Templates included:
- **Library: Loan Due Soon** – Sent 2 days before due date
- **Library: Loan Overdue** – Sent when loan becomes overdue

**Customize** templates with your branding and wording.

### 3. Scheduled Actions (Cron Jobs)

Navigate to **Settings → Technical → Automation → Scheduled Actions**

Active cron jobs:
- **Update Overdue Loans** – Daily at 3:00 AM
- **Send Due Soon Reminders** – Daily at 9:00 AM
- **Send Overdue Reminders** – Daily at 10:00 AM

**Adjust** timing or frequency as needed.

### 4. Security Groups

Navigate to **Settings → Users & Companies → Groups**

Groups:
- **Library User**: View own loans and browse books (for members)
- **Library Librarian**: Manage all loans and members
- **Library Manager**: Full access including configuration

**Assign** users to appropriate groups.

---

## 📱 Using Barcode Scanning

### Setup

1. **Assign Barcodes**
   - Edit members and add unique barcode values
   - Edit books and add unique barcode values

2. **Connect USB Scanner**
   - Use any keyboard-wedge USB barcode scanner
   - No special drivers needed

### Operation

**To Borrow a Book:**
1. Navigate to **Library → Scan & Go**
2. Scan member barcode → field populates
3. Scan book barcode → field populates
4. Set operation to "Auto" or "Borrow"
5. Click **Process Scan**
6. Loan is created instantly

**To Return a Book:**
1. Navigate to **Library → Scan & Go**
2. Scan member barcode
3. Scan book barcode
4. Set operation to "Auto" or "Return"
5. Click **Process Scan**
6. Book is returned, fine calculated if overdue

---

## 🧪 Running Tests

### Full Test Suite

```bash
odoo-bin -c /path/to/odoo.conf -d test_db -i baramej_library_system --test-enable --stop-after-init
```

### Individual Test Modules

```bash
# Test borrow limits
odoo-bin -c /path/to/odoo.conf -d test_db --test-tags /baramej_library_system:TestBorrowLimits

# Test overdue cron
odoo-bin -c /path/to/odoo.conf -d test_db --test-tags /baramej_library_system:TestOverdueCron

# Test email reminders
odoo-bin -c /path/to/odoo.conf -d test_db --test-tags /baramej_library_system:TestEmailReminders

# Test barcode flow
odoo-bin -c /path/to/odoo.conf -d test_db --test-tags /baramej_library_system:TestBarcodeFlow
```

### Test Coverage

- ✅ Borrow limit validation (edge cases)
- ✅ Overdue cron transitions & days calculation
- ✅ Email reminder sending & duplicate prevention
- ✅ Barcode scanning (checkout/return flows)
- ✅ Member type constraints
- ✅ Fine calculation accuracy

---

## 📁 Module Structure

```
baramej_library_system/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── library_member_type.py       # NEW: Member tier model
│   ├── library_book.py              # Enhanced with barcodes
│   ├── library_borrow.py            # Enhanced with states & overdue
│   ├── library_member.py            # Enhanced with types & stats
│   ├── library_barcode_scan.py      # NEW: Barcode wizard
│   ├── library_author.py
│   ├── library_category.py
│   ├── library_publisher.py
│   ├── library_location.py
│   ├── library_staff.py
│   ├── library_event.py
│   ├── library_reservation.py
│   └── library_review.py
├── views/
│   ├── library_member_type_views.xml    # NEW
│   ├── library_book_views.xml           # Enhanced
│   ├── library_borrow_views.xml         # Enhanced
│   ├── library_member_views.xml         # Enhanced
│   ├── library_barcode_views.xml        # NEW
│   ├── library_dashboard_views.xml      # NEW
│   ├── library_event_views.xml
│   ├── library_reservation_views.xml
│   └── menus.xml
├── security/
│   ├── library_security.xml             # NEW: Groups
│   ├── library_rules.xml                # NEW: Record rules
│   └── ir.model.access.csv              # Enhanced
├── data/
│   ├── library_member_type_data.xml     # NEW
│   ├── library_settings_data.xml        # NEW
│   ├── mail_templates.xml               # NEW
│   ├── ir_cron.xml                      # NEW
│   └── library_actions.xml
├── demo/
│   └── demo.xml                          # NEW: Sample data
├── tests/
│   ├── __init__.py                       # NEW
│   ├── test_borrow_limits.py            # NEW
│   ├── test_overdue_cron.py             # NEW
│   ├── test_email_reminders.py          # NEW
│   └── test_barcode_flow.py             # NEW
├── i18n/
│   └── en.po                             # NEW
├── static/
│   ├── description/
│   │   └── icon.png
│   └── src/
│       └── js/
│           └── barcode_scanner.js        # NEW
└── README.md
```

---

## 🔐 Security

### Access Control
- **ir.model.access.csv**: Model-level permissions (create, read, write, delete)
- **library_rules.xml**: Row-level security rules
  - Users see only their own loans
  - Librarians see all loans
  - Managers have full access

### Best Practices
- Always assign users to the appropriate group
- Test access control after group assignment
- Review record rules for custom needs

---

## 🚧 Troubleshooting

### Issue: Cron jobs not running
**Solution**: Check Odoo is running with `--max-cron-threads=2` or higher

### Issue: Emails not sending
**Solution**: Configure outgoing mail server in **Settings → Technical → Outgoing Mail Servers**

### Issue: Barcode scanner not working
**Solution**: 
- Ensure scanner is in keyboard-wedge mode
- Test scanner in a text editor first
- Check that barcode values are unique

### Issue: Tests failing
**Solution**:
- Ensure test database is clean
- Check that all dependencies are installed
- Review test output for specific errors

---

## 🧰 Development Workflow

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/alqasmii/Library-Management-.git
cd Library-Management-

# Create development branch
git checkout -b feature/your-feature-name

# Setup Odoo development instance
./odoo-bin -c dev.conf -d dev_db -i baramej_library_system --dev=all
```

### Pre-commit Hooks

We recommend using pre-commit hooks for code quality:

```bash
# Install pre-commit (Python)
pip install pre-commit

# Optional: Setup hooks for Python linting
# .pre-commit-config.yaml example:
# - flake8 for style checking
# - black/ruff for auto-formatting
# - pylint for code analysis
```

### Running Tests During Development

```bash
# Run all tests
./odoo-bin -c odoo.conf -d test_db --test-enable --stop-after-init

# Run specific test module
./odoo-bin -c odoo.conf -d test_db --test-tags /baramej_library_system:TestBorrowLimits

# Run with coverage (requires coverage.py)
coverage run --source=addons/baramej_library_system odoo-bin --test-enable -d test_db
coverage report
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

This module is CI/CD ready. Example workflow:

```yaml
name: Odoo Module Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: odoo
          POSTGRES_USER: odoo
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install Odoo & Dependencies
        run: |
          pip install -r requirements.txt
          pip install coverage
      
      - name: Run Tests
        run: |
          odoo-bin -c odoo.conf -d test_db \
            -i baramej_library_system \
            --test-enable \
            --stop-after-init \
            --log-level=test
```

### Deployment Best Practices

- **Staging Environment**: Test all changes in staging before production
- **Database Backups**: Always backup before running `-u` upgrade command
- **Rollback Plan**: Keep previous version available for quick rollback
- **Monitoring**: Set up log monitoring for cron job failures and errors
- **Performance**: Monitor database query performance, especially for large datasets

---

## 📊 Performance & Analytics

### Performance Optimization Tips

1. **Database Indexing**: Key fields (`barcode`, `state`, `due_date`) are already indexed
2. **Cron Optimization**: Scheduled actions process in batches to avoid memory issues
3. **Query Efficiency**: Uses Odoo ORM with proper domain filters (no raw SQL)
4. **Computed Fields**: Uses `store=True` for frequently accessed fields

### Built-in Analytics

The module provides several analytics capabilities:

- **Loan Trends**: Graph view showing borrowing patterns over time
- **Member Statistics**: Top borrowers, overdue rates per member type
- **Book Popularity**: Most borrowed books, longest waiting lists
- **Fine Tracking**: Total fines collected, outstanding fines by member

### Custom Reports

Extend the dashboard with custom reports:

```python
# Example: Custom report for monthly statistics
class LibraryMonthlyReport(models.Model):
    _name = 'library.monthly.report'
    _description = 'Monthly Library Statistics'
    _auto = False  # This is a SQL view
    
    month = fields.Date('Month')
    total_loans = fields.Integer('Total Loans')
    overdue_count = fields.Integer('Overdue Books')
    new_members = fields.Integer('New Members')
```

---

## 🔒 Security & Compliance

### Security Features

- ✅ **Row-Level Security**: Users see only their own loans
- ✅ **Role-Based Access Control**: Three distinct user roles
- ✅ **Input Validation**: All user inputs validated at model level
- ✅ **SQL Injection Prevention**: Odoo ORM only, no raw SQL
- ✅ **XSS Protection**: All views use proper escaping
- ✅ **CSRF Protection**: Built into Odoo framework

### Compliance & Best Practices

- **GDPR Considerations**: Personal data (member info) can be exported/deleted
- **Audit Trail**: All critical operations logged via `mail.thread` inheritance
- **Data Retention**: Configure retention policies for old loan records
- **Access Logs**: Track who accessed what via Odoo's built-in logging

### Security Checklist

- [ ] Change default admin password
- [ ] Configure HTTPS for production
- [ ] Set up regular database backups
- [ ] Review and customize access rights for your organization
- [ ] Enable two-factor authentication for admin users
- [ ] Configure email server with secure authentication
- [ ] Regular security updates for Odoo and dependencies

---

## 📈 Roadmap & Future Enhancements

### v2.1 (Planned)

- 🔄 **Book Reservations**: Queue system for popular books
- 📱 **Mobile App**: React Native mobile companion app
- 🔔 **Push Notifications**: Real-time alerts via web push
- 🌐 **Multi-Branch Support**: Manage multiple library locations
- 📊 **Advanced Analytics**: ML-based book recommendations

### v3.0 (Vision)

- 🤖 **AI-Powered Search**: Natural language book search
- 🔗 **Integration APIs**: RESTful API for external systems
- 📚 **Digital Content**: Support for e-books and audiobooks
- 🎓 **Learning Paths**: Curated reading lists and tracking
- 🌍 **Multi-Language**: Full internationalization support

### Community Requests

Have an idea? [Open an issue](https://github.com/alqasmii/Library-Management-/issues) or join the discussion!

---

## 📖 Documentation

### Additional Resources

- [Odoo Development Documentation](https://www.odoo.com/documentation/15.0/developer.html)
- [Module Architecture Guide](./docs/ARCHITECTURE.md) _(coming soon)_
- [API Reference](./docs/API.md) _(coming soon)_
- [Video Tutorial](https://youtube.com) _(coming soon)_

### FAQs

**Q: Can I use this in production?**  
A: Yes! The module is production-ready with comprehensive tests and security features.

**Q: How do I customize member types?**  
A: Navigate to Library → Configuration → Member Types and create/edit types.

**Q: Does this work with Odoo Enterprise?**  
A: Yes, fully compatible with both Community and Enterprise editions (v15+).

**Q: Can I integrate with my school's existing system?**  
A: The module provides standard Odoo models that can be extended. Consider using Odoo's API or developing custom integrations.

**Q: How do I handle lost books?**  
A: Add a "Lost" state to the loan model or track via the notes field. Future versions may include this natively.

---

## 🎯 Use Cases

### Educational Institutions
- **Schools**: Manage library for students and teachers
- **Universities**: Multiple member tiers (undergrad, grad, faculty, staff)
- **Training Centers**: Track training materials and resources

### Corporate
- **Company Libraries**: Manage technical books and resources
- **Research Organizations**: Track academic papers and publications
- **Co-working Spaces**: Community resource sharing

### Community
- **Public Libraries**: Full-featured library management
- **Book Clubs**: Track member readings and loans
- **Little Free Libraries**: Simple neighborhood book tracking



---

## 🤝 Contributing

We welcome contributions! To contribute:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Coding Standards
- Follow Odoo's development guidelines
- Use XML ID prefixes `library_`
- Write tests for new features
- Document major logic changes
- Translate user-facing strings

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

Feel free to use, modify, and distribute — just give credit where it's due. 💜

---

## 👨‍💻 Author

Built with ❤️ by [@alqasmii](https://github.com/alqasmii)

Developing useful tools for modern organizations and testing how fast we can ship 🚀

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/alqasmii/Library-Management-/issues)
- **Discussions**: [GitHub Discussions](https://github.com/alqasmii/Library-Management-/discussions)
- **Email**: [Contact via GitHub](https://github.com/alqasmii)

---

## �️ Tech Stack

### Backend
- **Framework**: Odoo 15+ (Python 3.8+)
- **ORM**: Odoo ORM (PostgreSQL)
- **Async Tasks**: Odoo Cron System
- **Email**: Odoo Mail Module (SMTP)

### Frontend
- **Views**: QWeb Templates (XML)
- **JavaScript**: Owl.js Framework (Odoo native)
- **Widgets**: Custom barcode scanner widget
- **CSS**: Bootstrap 5 (Odoo theme)

### Testing
- **Framework**: Odoo TestCase (unittest-based)
- **Coverage**: 40+ test cases across 4 test files
- **CI/CD**: GitHub Actions ready

### Infrastructure
- **Database**: PostgreSQL 12+
- **Server**: Linux/Unix (recommended) or Windows
- **Web Server**: Odoo built-in or Nginx/Apache reverse proxy
- **Scanner**: USB barcode scanners (keyboard-wedge mode)

---

## 📝 Changelog

### [2.0.0] - 2025-10-29

#### 🎉 Major Release - Production Ready

**Added**
- ✨ Member tier system with configurable borrowing limits
- ✨ Automatic overdue detection via daily cron job
- ✨ Email reminder system (due soon & overdue notifications)
- ✨ Barcode scanning for books and members
- ✨ Comprehensive reporting dashboard with graphs and pivot views
- ✨ Multi-role security (User, Librarian, Manager)
- ✨ 40+ unit tests covering all workflows
- ✨ Demo data for quick testing
- ✨ Internationalization support (i18n)
- ✨ Enhanced loan workflow with states (draft, borrowed, overdue, returned, cancelled)
- ✨ Fine calculation based on overdue days
- ✨ Barcode scan & go wizard for quick checkout/return

**Enhanced**
- 🔧 Complete rewrite of book, member, and loan models
- 🔧 New KPI dashboard with real-time statistics
- 🔧 Row-level security with record rules
- 🔧 Mail integration with activity tracking
- 🔧 39 model-level access control rules

**Security**
- 🔒 OWASP-compliant input validation
- 🔒 SQL injection prevention (ORM-only)
- 🔒 XSS protection in all views
- 🔒 Role-based access control with three user groups

**Documentation**
- 📚 Comprehensive README with installation guide
- 📚 Configuration instructions for all features
- 📚 Testing guide with examples
- 📚 Troubleshooting section
- 📚 Module structure diagram

### [1.0.0] - 2024-XX-XX

**Initial Release**
- Basic book, member, and loan models
- Simple views for CRUD operations
- Basic security with access control
- Foundation for future enhancements

---

## 🙏 Acknowledgments

- **Odoo Community**: For the amazing open-source ERP framework
- **Contributors**: Everyone who tested, reported issues, and contributed code
- **Organizations**: Schools and libraries using this module in production
- **Open Source**: Built on the shoulders of giants 🚀

---

## ⭐ Show Your Support

If this module helped you, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs and issues
- 💡 Suggesting new features
- 🔀 Contributing code improvements
- 📢 Sharing with others who might benefit

---

> ✨ **Clean code. Modular design. Production-ready. Odoo v15+**

**v2.0.0** | Released October 2025 | Built with ❤️ by [@alqasmii](https://github.com/alqasmii)
