import { useState, useRef } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLang } from '../context/LangContext';
import { GlassCard, GlassInput, GlassButton } from '../components/ui';
import api from '../api/axios';

export default function Profile() {
  const { user, loading, refreshUser } = useAuth();
  const { t } = useLang();
  const fileRef = useRef<HTMLInputElement>(null);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({ first_name: '', last_name: '', phone_number: '' });

  if (loading) return <div style={{ paddingTop: 160, textAlign: 'center', color: 'var(--text-muted)' }}>...</div>;
  if (!user) return <Navigate to="/login" />;

  const startEdit = () => { setForm({ first_name: user.first_name || '', last_name: user.last_name || '', phone_number: user.phone_number || '' }); setEditing(true); };
  const save = async () => { setSaving(true); try { await api.patch(`/users/${user.id}/`, form); await refreshUser(); setEditing(false); } catch {} setSaving(false); };
  const upload = async (e: React.ChangeEvent<HTMLInputElement>) => { const f = e.target.files?.[0]; if (!f) return; const fd = new FormData(); fd.append('avatar', f); await api.patch(`/users/${user.id}/`, fd, { headers: { 'Content-Type': 'multipart/form-data' } }); await refreshUser(); };

  return (<div className="profilePage"><GlassCard className="profileCard">
    <div className="profileTop">
      <div className="profilePic" onClick={() => fileRef.current?.click()}>
        {user.avatar ? <img src={`http://127.0.0.1:8000${user.avatar}`} alt="" /> : user.username?.[0]?.toUpperCase()}
        <input ref={fileRef} type="file" accept="image/*" onChange={upload} style={{ display: 'none' }} />
      </div>
      <div className="profileInfo"><h2>{user.first_name || user.username}</h2><p>@{user.username} · {user.subscription_status === 'VIP' ? '★ VIP' : 'Free'}</p></div>
    </div>
    {editing ? (<div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
        <GlassInput placeholder="Имя" value={form.first_name} onChange={e => setForm({...form, first_name: e.target.value})} style={{ marginTop: 0 }} />
        <GlassInput placeholder="Фамилия" value={form.last_name} onChange={e => setForm({...form, last_name: e.target.value})} style={{ marginTop: 0 }} />
      </div>
      <GlassInput placeholder="Телефон" value={form.phone_number} onChange={e => setForm({...form, phone_number: e.target.value})} />
      <div style={{ display: 'flex', gap: 10 }}>
        <GlassButton style={{ flex: 1 }} onClick={save} disabled={saving}>{saving ? '...' : 'Сохранить'}</GlassButton>
        <button className="btnGhost" onClick={() => setEditing(false)}>Отмена</button>
      </div>
    </div>) : (<div>
      <div className="profileField"><label>Email</label><span>{user.email}</span></div>
      {user.first_name && <div className="profileField"><label>Имя</label><span>{user.first_name}</span></div>}
      {user.last_name && <div className="profileField"><label>Фамилия</label><span>{user.last_name}</span></div>}
      {user.phone_number && <div className="profileField"><label>Телефон</label><span>{user.phone_number}</span></div>}
      <button className="btnGhost" style={{ marginTop: 12 }} onClick={startEdit}>{t('Редактировать', 'Өзгөртүү', 'Tahrir')}</button>
    </div>)}
  </GlassCard></div>);
}
