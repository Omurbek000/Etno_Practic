import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { bumpLangVersion } from '../api/axios';

type Lang = 'ru' | 'ky' | 'uz';
interface LangContextType { lang: Lang; setLang: (l: Lang) => void; langVersion: number; t: (ru: string, ky: string, uz: string) => string; }

const LangContext = createContext<LangContextType>({} as LangContextType);
export const useLang = () => useContext(LangContext);

export function LangProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(() => (localStorage.getItem('etno_lang') as Lang) || 'ru');
  const [langVersion, setLangVersion] = useState(0);
  const setLang = (l: Lang) => { setLangState(l); localStorage.setItem('etno_lang', l); bumpLangVersion(); setLangVersion(v => v + 1); };
  const t = (ru: string, ky: string, uz: string) => lang === 'ky' ? ky : lang === 'uz' ? uz : ru;
  useEffect(() => { document.documentElement.lang = lang; }, [lang]);
  return <LangContext.Provider value={{ lang, setLang, langVersion, t }}>{children}</LangContext.Provider>;
}
