import type { ReactNode } from 'react';

export function GlassCard({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <div className={`glass-card ${className}`}>{children}</div>;
}

export function GlassTitle({ children }: { children: ReactNode }) {
  return <h1 className="glass-title">{children}</h1>;
}

export function GlassInput(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return <input className="glass-input" {...props} />;
}

export function GlassButton({ children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button className="glass-button" {...props}>{children}</button>;
}
