# Duplicate Registration Prevention System

## Overview

The system prevents duplicate registrations using **hash-based comparison** instead of direct encrypted value comparison. This approach is more reliable and handles edge cases better.

## How It Works

### 1. Hash-Based Comparison
- Uses SHA256 hashing to create consistent, comparable values
- Normalizes data (lowercase, strip whitespace) before hashing
- Compares hashes instead of encrypted values

### 2. Validation Process

#### Email Validation:
1. Normalize email (lowercase, strip whitespace)
2. Create SHA256 hash of normalized email
3. Decrypt all existing student emails
4. Hash each existing email and compare
5. Reject if hash matches any existing record

#### Mobile Validation:
1. Extract digits only from mobile number
2. Create SHA256 hash of digits
3. Decrypt all existing student mobile numbers
4. Extract digits and hash each existing mobile
5. Reject if hash matches any existing record

#### Cross-Field Validation:
- Checks if both email AND mobile match the same existing student
- Provides specific error message for this case

## Implementation Details

### Files Modified:

1. **`core/students/encryption.py`**
   - Added `hash_for_comparison()` function
   - Creates SHA256 hash of normalized data

2. **`core/students/forms.py`**
   - Updated `clean_email()` - hash-based duplicate check
   - Updated `clean_mobile()` - hash-based duplicate check
   - Added `clean()` - cross-field validation

3. **`core/students/views.py`**
   - Enhanced error handling for duplicate entries
   - Better error messages for users

## Error Messages

### Email Duplicate:
```
"This email address is already registered. Please use a different email address or contact support if you believe this is an error."
```

### Mobile Duplicate:
```
"This mobile number is already registered. Please use a different mobile number."
```

### Both Match Same Student:
```
"A registration with this email and mobile number combination already exists. Please use different contact information or contact support."
```

## Why Hash-Based?

### Advantages:
1. **Consistent Comparison**: Same input always produces same hash
2. **Case Insensitive**: Normalization handles case differences
3. **Format Independent**: Mobile numbers compared by digits only
4. **Reliable**: Works even if encryption produces different ciphertexts (though Fernet is deterministic)

### Example:
- Email: `John@Example.com` → normalized → `john@example.com` → hash
- Email: `JOHN@EXAMPLE.COM` → normalized → `john@example.com` → same hash ✅

- Mobile: `+1 (555) 123-4567` → digits → `15551234567` → hash
- Mobile: `1555-123-4567` → digits → `15551234567` → same hash ✅

## Testing

### Test Cases:
1. ✅ Same email (different case) - Rejected
2. ✅ Same mobile (different format) - Rejected
3. ✅ Same email + mobile combination - Rejected with specific message
4. ✅ Different email, same mobile - Rejected (mobile duplicate)
5. ✅ Same email, different mobile - Rejected (email duplicate)
6. ✅ All different - Accepted

## Performance Considerations

- Current implementation decrypts all records for comparison
- For large datasets (1000+ records), consider:
  - Adding hash columns to database table
  - Using database indexes on hash columns
  - Caching hash values

## Security Notes

- Hashes are one-way (cannot reverse to original data)
- Used only for comparison, not storage
- Original data remains encrypted in database
- Hash comparison happens server-side only
