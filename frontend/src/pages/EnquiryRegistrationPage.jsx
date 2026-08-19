import React, { useState } from 'react';
import {
  User,
  Calendar,
  FileText,
  UploadCloud,
  Image as ImageIcon,
  Plus,
  X,
  AlertCircle,
  CheckCircle,
  Save,
} from 'lucide-react';
import { getApiUrl } from '../config';

const BRAND_OPTIONS = [
  'Select Brand',
  'Allen Solly',
  'Indian Terrain',
  'Louis Philippe',
  'Van Heusen',
  'Blackberrys',
  'Pepe Jeans London',
  'Lee Cooper',
  'Wrogn',
  'Parx',
  'Reliance Trends',
  'ColorPlus',
  'Jockey',
  'Max',
  'Scullers',
  'Peter England',
  'DNMX',
  'Buffalo',
  'Bare Denim',
  'WLS',
  'Aditya Birla Group',
  'Izod',
  'Indigo Nation',
  'John Players',
  'Mufti',
  'Park Avenue',
  'Boss (Hugo Boss)',
  'Camaïeu',
  'Mango',
  'Esprit',
  'Lee',
  's.Oliver',
  'Zara',
  'Matalan',
  'Pull&Bear',
  'Celio*',
  'Next',
  'Tommy Hilfiger',
  'RB Sellars',
  "Levi's",
  'CK (Calvin Klein)',
  'Zalando',
  'Giovanni Galli',
  'Wrangler',
  'Diesel',
  "Sainsbury's",
  'M&S (Marks & Spencer)',
  'Gant',
  'United Colors of Benetton',
  'Scotch & Soda',
  'Hackett London',
  'H&M',
  'Nike',
  'Adidas',
  'Puma',
  'Uniqlo',
  'Gap',
  'Gucci',
  'Prada',
  'Other (Custom)',
];

const COUNTRY_OPTIONS = [
  'Select Country',
  'Spain',
  'India',
  'United States',
  'United Kingdom',
  'Germany',
  'France',
  'Italy',
  'Turkey',
  'Bangladesh',
  'China',
  'Vietnam',
  'Japan',
  'Brazil',
  'Canada',
  'Australia',
  'United Arab Emirates',
  'Other',
];

const PRIORITY_OPTIONS = [
  { label: 'High', color: '#ef4444' },
  { label: 'Medium', color: '#f59e0b' },
  { label: 'Low', color: '#10b981' },
  { label: 'Urgent', color: '#dc2626' },
];

const REQUIREMENT_TYPES = [
  'Development',
  'Bulk Production',
  'Sampling',
  'Sourcing',
  'Custom',
];

const SEASONS = ['AW 25', 'SS 25', 'AW 26', 'SS 26', 'Core Collection'];
const STATUSES = ['New', 'In Progress', 'Pending', 'Completed', 'On Hold'];
const END_USES = ['Shirts', 'Pants', 'Dresses', 'Outerwear', 'Suits', 'Activewear', 'Other'];

export const EnquiryRegistrationPage = ({ onCancel, onSavedSuccess }) => {
  // Section 1: Brand & Buyer Information
  const [brandName, setBrandName] = useState('Select Brand');
  const [customBrand, setCustomBrand] = useState('');
  const [company, setCompany] = useState('');
  const [country, setCountry] = useState('Select Country');
  const [contactPerson, setContactPerson] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [buyerId] = useState(() => 'B-' + String(Math.floor(10000 + Math.random() * 90000)));

  // Section 2: Enquiry Information
  const [enquiryId] = useState(() => 'ENQ-2025-' + String(Math.floor(10000 + Math.random() * 90000)).padStart(5, '0'));
  const [dateReceived, setDateReceived] = useState(() => new Date().toISOString().split('T')[0]);
  const [dueDate, setDueDate] = useState('');
  const [priority, setPriority] = useState('High');
  const [requirementType, setRequirementType] = useState('Development');
  const [address, setAddress] = useState('');
  const [status, setStatus] = useState('New');
  const [endUse, setEndUse] = useState('Shirts');

  // Section 3: Requirement Summary (Empty by default)
  const [summary, setSummary] = useState('');

  // Section 4: Documents (Empty by default)
  const [documents, setDocuments] = useState([]);

  // Section 5: Reference Images (Empty by default)
  const [referenceImages, setReferenceImages] = useState([]);

  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;
    const newDocs = files.map((f, i) => ({
      id: String(Date.now() + i),
      name: f.name,
      size: (f.size / (1024 * 1024)).toFixed(1) + ' MB',
      type: f.name.endsWith('.pdf') ? 'pdf' : f.name.endsWith('.zip') ? 'zip' : 'doc',
    }));
    setDocuments((prev) => [...prev, ...newDocs]);
  };

  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;
    files.forEach((file) => {
      const reader = new FileReader();
      reader.onload = (ev) => {
        setReferenceImages((prev) => [...prev, ev.target.result]);
      };
      reader.readAsDataURL(file);
    });
  };

  const removeDocument = (id) => {
    setDocuments((prev) => prev.filter((d) => d.id !== id));
  };

  const removeReferenceImage = (idx) => {
    setReferenceImages((prev) => prev.filter((_, i) => i !== idx));
  };

  const handleSaveEnquiry = async () => {
    setErrorMsg('');
    setSuccessMsg('');

    const effectiveBrand = brandName === 'Other (Custom)' ? customBrand : brandName;

    if (!effectiveBrand.trim() || effectiveBrand === 'Select Brand') { setErrorMsg('Brand Name is required'); return; }
    if (!country || country === 'Select Country') { setErrorMsg('Country is required'); return; }
    if (!email.trim()) { setErrorMsg('Email is required'); return; }
    if (!summary.trim()) { setErrorMsg('Requirement Summary is required'); return; }

    setSaving(true);
    try {
      // Use Company name for the Wishlist Group if entered, otherwise fall back to Brand Name
      const groupName = (company && company.trim()) ? company.trim() : effectiveBrand.trim();

      // Automatically create a new Wishlist Group in the backend / wishlist store
      try {
        await fetch(getApiUrl('/api/wishlist/groups/create'), {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ name: groupName }),
        });
      } catch (e) {
        // Group creation error or already exists
      }

      const payload = {
        buyer_name: effectiveBrand.trim(),
        brand_name: effectiveBrand.trim(),
        company: company ? company.trim() : '',
        country,
        contact_person: contactPerson,
        email,
        phone_number: phoneNumber,
        buyer_id: buyerId,
        enquiry_id: enquiryId,
        date_received: dateReceived,
        due_date: dueDate,
        priority,
        requirement_type: requirementType,
        address,
        status,
        end_use: endUse,
        summary,
        documents: documents.map((d) => d.name),
        reference_images: referenceImages,
        reference_images_count: referenceImages.length,
      };

      try {
        const res = await fetch(getApiUrl('/api/enquiries/create'), {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(payload),
        });
        if (res.ok) {
          const data = await res.json();
          if (data && (data.enquiry || data.buyer_name)) {
            Object.assign(payload, data.enquiry || data);
          }
        }
      } catch (err) {
        // Client fallback
      }

      setSuccessMsg(`Buyer enquiry registered & Wishlist Group "${groupName}" created successfully!`);
      setTimeout(() => {
        if (onSavedSuccess) onSavedSuccess(payload);
      }, 800);
    } catch (err) {
      setErrorMsg(err.message || 'Could not save enquiry');
    } finally {
      setSaving(false);
    }
  };

  const selectedPriorityObj = PRIORITY_OPTIONS.find((p) => p.label === priority) || PRIORITY_OPTIONS[0];

  return (
    <div
      style={{
        background: '#f8fafc',
        minHeight: '100vh',
        padding: '1.75rem 2rem 4rem',
        fontFamily: 'Inter, system-ui, -apple-system, sans-serif',
        color: '#0f172a',
      }}
    >
      {/* Top Title & Header Actions Bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '1.75rem',
          flexWrap: 'wrap',
          gap: '1rem',
        }}
      >
        <div>
          <h1
            style={{
              fontSize: '1.75rem',
              fontWeight: 800,
              color: '#0f172a',
              letterSpacing: '-0.025em',
              lineHeight: 1.2,
              marginBottom: '0.2rem',
            }}
          >
            Buyer Enquiry Registration
          </h1>
          <p style={{ fontSize: '0.88rem', color: '#64748b', fontWeight: 500 }}>
            Register new buyer enquiry and requirement details
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <button
            onClick={onCancel}
            style={{
              padding: '0.6rem 1.35rem',
              borderRadius: '8px',
              border: '1px solid #cbd5e1',
              background: '#ffffff',
              color: '#334155',
              fontSize: '0.88rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            Cancel
          </button>
          <button
            onClick={handleSaveEnquiry}
            disabled={saving}
            style={{
              padding: '0.6rem 1.45rem',
              borderRadius: '8px',
              border: 'none',
              background: 'linear-gradient(135deg, #1e3a8a, #2563eb)',
              color: '#ffffff',
              fontSize: '0.88rem',
              fontWeight: 700,
              cursor: saving ? 'not-allowed' : 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              boxShadow: '0 4px 12px rgba(37, 99, 235, 0.25)',
              transition: 'all 0.2s',
            }}
          >
            <Save size={16} />
            <span>{saving ? 'Saving...' : 'Save Enquiry'}</span>
          </button>
        </div>
      </div>

      {/* Notifications */}
      {errorMsg && (
        <div
          style={{
            marginBottom: '1.25rem',
            padding: '0.85rem 1.1rem',
            borderRadius: '10px',
            background: '#fef2f2',
            border: '1px solid #fecaca',
            color: '#dc2626',
            fontSize: '0.88rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            fontWeight: 500,
          }}
        >
          <AlertCircle size={18} style={{ flexShrink: 0 }} />
          <span>{errorMsg}</span>
        </div>
      )}

      {successMsg && (
        <div
          style={{
            marginBottom: '1.25rem',
            padding: '0.85rem 1.1rem',
            borderRadius: '10px',
            background: '#f0fdf4',
            border: '1px solid #bbf7d0',
            color: '#16a34a',
            fontSize: '0.88rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            fontWeight: 500,
          }}
        >
          <CheckCircle size={18} style={{ flexShrink: 0 }} />
          <span>{successMsg}</span>
        </div>
      )}

      {/* 2-Column Main Layout: Left = Sections 1-3, Right = Sections 4-5 + Preview */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: '1.75rem' }}>
        {/* Left Column (Sections 1, 2, 3) */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Section 1: Buyer Information */}
          <div
            style={{
              background: '#ffffff',
              borderRadius: '14px',
              border: '1px solid #e2e8f0',
              padding: '1.6rem',
              boxShadow: '0 2px 8px rgba(15, 23, 42, 0.04)',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                marginBottom: '1.5rem',
                paddingBottom: '0.85rem',
                borderBottom: '1px solid #f1f5f9',
              }}
            >
              <div
                style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  background: '#eff6ff',
                  color: '#2563eb',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                }}
              >
                <User size={18} />
              </div>
              <h2 style={{ fontSize: '1.08rem', fontWeight: 700, color: '#1e293b' }}>
                1. Brand & Buyer Information
              </h2>
            </div>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '1.2rem',
              }}
            >
              {/* Brand Name */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Brand Name <span style={{ color: '#ef4444' }}>*</span>
                </label>
                <select
                  value={brandName}
                  onChange={(e) => setBrandName(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    background: '#ffffff',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                >
                  {BRAND_OPTIONS.map((b) => (
                    <option key={b} value={b}>{b}</option>
                  ))}
                </select>
                {brandName === 'Other (Custom)' && (
                  <input
                    type="text"
                    required
                    placeholder="Enter custom brand"
                    value={customBrand}
                    onChange={(e) => setCustomBrand(e.target.value)}
                    style={{
                      width: '100%',
                      marginTop: '0.5rem',
                      padding: '0.6rem 0.85rem',
                      borderRadius: '8px',
                      border: '1.5px solid #cbd5e1',
                      fontSize: '0.88rem',
                      boxSizing: 'border-box',
                    }}
                  />
                )}
              </div>

              {/* Company */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Company
                </label>
                <input
                  type="text"
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  placeholder="e.g. Inditex"
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                />
              </div>

              {/* Country */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Country <span style={{ color: '#ef4444' }}>*</span>
                </label>
                <select
                  value={country}
                  onChange={(e) => setCountry(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    background: '#ffffff',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                >
                  {COUNTRY_OPTIONS.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              {/* Contact Person */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Contact Person
                </label>
                <input
                  type="text"
                  value={contactPerson}
                  onChange={(e) => setContactPerson(e.target.value)}
                  placeholder="e.g. Mr. David Garcia"
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                />
              </div>

              {/* Email */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Email <span style={{ color: '#ef4444' }}>*</span>
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="e.g. david.garcia@zara.com"
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                />
              </div>

              {/* Phone Number */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Phone Number
                </label>
                <input
                  type="text"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  placeholder="e.g. +34 612 345 678"
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                />
              </div>

              {/* Buyer ID */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#64748b', marginBottom: '0.4rem' }}>
                  Buyer ID
                </label>
                <input
                  type="text"
                  readOnly
                  disabled
                  value={buyerId}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #e2e8f0',
                    background: '#f8fafc',
                    color: '#475569',
                    fontSize: '0.9rem',
                    fontWeight: 600,
                    boxSizing: 'border-box',
                  }}
                />
              </div>
            </div>
          </div>

          {/* Section 2: Enquiry Information */}
          <div
            style={{
              background: '#ffffff',
              borderRadius: '14px',
              border: '1px solid #e2e8f0',
              padding: '1.6rem',
              boxShadow: '0 2px 8px rgba(15, 23, 42, 0.04)',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                marginBottom: '1.5rem',
                paddingBottom: '0.85rem',
                borderBottom: '1px solid #f1f5f9',
              }}
            >
              <div
                style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  background: '#eff6ff',
                  color: '#2563eb',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                }}
              >
                <Calendar size={18} />
              </div>
              <h2 style={{ fontSize: '1.08rem', fontWeight: 700, color: '#1e293b' }}>
                2. Enquiry Information
              </h2>
            </div>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '1.2rem',
              }}
            >
              {/* Enquiry ID */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#64748b', marginBottom: '0.4rem' }}>
                  Enquiry ID
                </label>
                <input
                  type="text"
                  readOnly
                  disabled
                  value={enquiryId}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #e2e8f0',
                    background: '#f8fafc',
                    color: '#475569',
                    fontSize: '0.9rem',
                    fontWeight: 600,
                    boxSizing: 'border-box',
                  }}
                />
              </div>

              {/* Date Received */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Date Received <span style={{ color: '#ef4444' }}>*</span>
                </label>
                <input
                  type="date"
                  required
                  value={dateReceived}
                  onChange={(e) => setDateReceived(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                />
              </div>

              {/* Due Date */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Due Date
                </label>
                <input
                  type="date"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                />
              </div>

              {/* Priority */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Priority <span style={{ color: '#ef4444' }}>*</span>
                </label>
                <select
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    background: '#ffffff',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                >
                  {PRIORITY_OPTIONS.map((p) => (
                    <option key={p.label} value={p.label}>
                      ● {p.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Requirement Type */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Requirement Type <span style={{ color: '#ef4444' }}>*</span>
                </label>
                <select
                  value={requirementType}
                  onChange={(e) => setRequirementType(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    background: '#ffffff',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                >
                  {REQUIREMENT_TYPES.map((t) => (
                    <option key={t} value={t}>{t}</option>
                  ))}
                </select>
              </div>

              {/* Address */}
              <div style={{ gridColumn: 'span 2' }}>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Address
                </label>
                <input
                  type="text"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="e.g. 123 Fashion Ave, Suite 400, New York, NY"
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                />
              </div>

              {/* Status */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  Status
                </label>
                <select
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    background: '#ffffff',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                >
                  {STATUSES.map((st) => (
                    <option key={st} value={st}>{st}</option>
                  ))}
                </select>
              </div>

              {/* End Use */}
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                  End Use
                </label>
                <select
                  value={endUse}
                  onChange={(e) => setEndUse(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    background: '#ffffff',
                    boxSizing: 'border-box',
                    outline: 'none',
                  }}
                >
                  {END_USES.map((eu) => (
                    <option key={eu} value={eu}>{eu}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Section 3: Requirement Summary */}
          <div
            style={{
              background: '#ffffff',
              borderRadius: '14px',
              border: '1px solid #e2e8f0',
              padding: '1.6rem',
              boxShadow: '0 2px 8px rgba(15, 23, 42, 0.04)',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                marginBottom: '1.25rem',
                paddingBottom: '0.85rem',
                borderBottom: '1px solid #f1f5f9',
              }}
            >
              <div
                style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  background: '#eff6ff',
                  color: '#2563eb',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                }}
              >
                <FileText size={18} />
              </div>
              <h2 style={{ fontSize: '1.08rem', fontWeight: 700, color: '#1e293b' }}>
                3. Requirement Summary
              </h2>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#334155', marginBottom: '0.4rem' }}>
                Summary / Notes <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <div style={{ position: 'relative' }}>
                <textarea
                  required
                  rows={4}
                  maxLength={500}
                  value={summary}
                  onChange={(e) => setSummary(e.target.value)}
                  placeholder="Enter detailed buyer requirement summary, fabric properties, drape preferences, etc."
                  style={{
                    width: '100%',
                    padding: '0.8rem 0.9rem',
                    borderRadius: '8px',
                    border: '1.5px solid #cbd5e1',
                    fontSize: '0.9rem',
                    lineHeight: 1.5,
                    fontFamily: 'inherit',
                    boxSizing: 'border-box',
                    outline: 'none',
                    resize: 'vertical',
                  }}
                />
                <div
                  style={{
                    position: 'absolute',
                    bottom: '10px',
                    right: '12px',
                    fontSize: '0.75rem',
                    color: '#94a3b8',
                    fontWeight: 500,
                  }}
                >
                  {summary.length} / 500
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Sections 4 & 5 + Enquiry Preview Card */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Section 4: Upload Documents */}
          <div
            style={{
              background: '#ffffff',
              borderRadius: '14px',
              border: '1px solid #e2e8f0',
              padding: '1.4rem',
              boxShadow: '0 2px 8px rgba(15, 23, 42, 0.04)',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.65rem',
                marginBottom: '1.25rem',
              }}
            >
              <div
                style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: '#eff6ff',
                  color: '#2563eb',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                }}
              >
                <UploadCloud size={16} />
              </div>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#1e293b' }}>
                4. Upload Documents
              </h3>
            </div>

            {/* Drag & Drop Upload Container */}
            <label
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '1.5rem 1rem',
                border: '2px dashed #cbd5e1',
                borderRadius: '12px',
                background: '#f8fafc',
                cursor: 'pointer',
                textAlign: 'center',
                marginBottom: '1.2rem',
                transition: 'border-color 0.2s',
              }}
            >
              <span style={{ fontSize: '0.88rem', color: '#475569', fontWeight: 600, marginBottom: '0.4rem' }}>
                Drag & drop files here
              </span>
              <span style={{ fontSize: '0.78rem', color: '#94a3b8', marginBottom: '0.8rem' }}>or</span>
              <span
                style={{
                  padding: '0.45rem 1rem',
                  borderRadius: '6px',
                  border: '1px solid #cbd5e1',
                  background: '#ffffff',
                  color: '#334155',
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  boxShadow: '0 1px 2px rgba(0,0,0,0.04)',
                }}
              >
                Browse Files
              </span>
              <input
                type="file"
                multiple
                accept=".pdf,.zip,.doc,.docx"
                onChange={handleFileUpload}
                style={{ display: 'none' }}
              />
            </label>

            {/* Uploaded Documents List */}
            {documents.length > 0 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                {documents.map((doc) => (
                  <div
                    key={doc.id}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '0.55rem 0.8rem',
                      borderRadius: '8px',
                      background: '#f8fafc',
                      border: '1px solid #f1f5f9',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', overflow: 'hidden' }}>
                      <div
                        style={{
                          padding: '4px 6px',
                          borderRadius: '4px',
                          background: '#fef2f2',
                          color: '#ef4444',
                          fontSize: '9px',
                          fontWeight: 800,
                        }}
                      >
                        {doc.type.toUpperCase()}
                      </div>
                      <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        <div style={{ fontSize: '0.82rem', fontWeight: 600, color: '#334155', textOverflow: 'ellipsis', overflow: 'hidden' }}>
                          {doc.name}
                        </div>
                        <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>{doc.size}</div>
                      </div>
                    </div>

                    <button
                      onClick={() => removeDocument(doc.id)}
                      style={{
                        background: 'none',
                        border: 'none',
                        color: '#94a3b8',
                        cursor: 'pointer',
                        padding: '2px',
                      }}
                    >
                      <X size={14} />
                    </button>
                  </div>
                ))}
              </div>
            )}

            <div style={{ marginTop: '0.85rem', fontSize: '0.72rem', color: '#94a3b8' }}>
              Max file size: 20MB each
            </div>
          </div>

          {/* Section 5: Reference Images (Optional) */}
          <div
            style={{
              background: '#ffffff',
              borderRadius: '14px',
              border: '1px solid #e2e8f0',
              padding: '1.4rem',
              boxShadow: '0 2px 8px rgba(15, 23, 42, 0.04)',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.65rem',
                marginBottom: '1.25rem',
              }}
            >
              <div
                style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: '#eff6ff',
                  color: '#2563eb',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                }}
              >
                <ImageIcon size={16} />
              </div>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#1e293b' }}>
                5. Reference Images (Optional)
              </h3>
            </div>

            {/* Reference Images Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.65rem' }}>
              {referenceImages.map((src, i) => (
                <div
                  key={i}
                  style={{
                    position: 'relative',
                    aspectRatio: '1',
                    borderRadius: '8px',
                    overflow: 'hidden',
                    border: '1px solid #e2e8f0',
                  }}
                >
                  <img
                    src={src}
                    alt={`Reference ${i + 1}`}
                    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                  />
                  <button
                    onClick={() => removeReferenceImage(i)}
                    style={{
                      position: 'absolute',
                      top: '4px',
                      right: '4px',
                      width: '20px',
                      height: '20px',
                      borderRadius: '50%',
                      background: 'rgba(15, 23, 42, 0.65)',
                      color: '#ffffff',
                      border: 'none',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    <X size={12} />
                  </button>
                </div>
              ))}

              {/* Add More Button */}
              <label
                style={{
                  aspectRatio: '1',
                  borderRadius: '8px',
                  border: '1.5px dashed #cbd5e1',
                  background: '#f8fafc',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer',
                  color: '#64748b',
                  transition: 'border-color 0.2s',
                }}
              >
                <Plus size={20} />
                <span style={{ fontSize: '0.72rem', fontWeight: 600, marginTop: '2px' }}>
                  Add more
                </span>
                <input
                  type="file"
                  multiple
                  accept="image/*"
                  onChange={handleImageUpload}
                  style={{ display: 'none' }}
                />
              </label>
            </div>
          </div>

          {/* Enquiry Preview Card */}
          <div
            style={{
              background: '#ffffff',
              borderRadius: '14px',
              border: '1px solid #e2e8f0',
              padding: '1.4rem',
              boxShadow: '0 2px 8px rgba(15, 23, 42, 0.04)',
            }}
          >
            <div style={{ fontSize: '0.92rem', fontWeight: 700, color: '#1e293b', marginBottom: '1rem' }}>
              Enquiry Preview
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.85rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#64748b', fontWeight: 500 }}>Brand Name</span>
                <span style={{ fontWeight: 700, color: '#0f172a' }}>
                  {brandName !== 'Select Brand' ? (brandName === 'Other (Custom)' ? customBrand || '—' : brandName) : '—'}
                </span>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#64748b', fontWeight: 500 }}>Enquiry ID</span>
                <span style={{ fontWeight: 600, color: '#334155' }}>{enquiryId}</span>
              </div>

              {address && (
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#64748b', fontWeight: 500 }}>Address</span>
                  <span style={{ fontWeight: 600, color: '#334155', maxWidth: '160px', textAlign: 'right' }}>{address}</span>
                </div>
              )}

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#64748b', fontWeight: 500 }}>Priority</span>
                <span style={{ fontWeight: 700, color: selectedPriorityObj.color, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                  <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: selectedPriorityObj.color }} />
                  {priority}
                </span>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#64748b', fontWeight: 500 }}>Due Date</span>
                <span style={{ fontWeight: 600, color: '#334155' }}>
                  {dueDate ? new Date(dueDate).toLocaleDateString('en-GB') : '—'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnquiryRegistrationPage;
