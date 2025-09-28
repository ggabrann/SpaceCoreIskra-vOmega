import re

from src.nia_autocalib import analyze as auto_analyze
from src.nia_core_ext import Guardian, load_modes
from src.nia_memory import write_short_term

ANCHOR_PATTERN = re.compile(r'#(?:a|t|ref|f):[A-Za-z0-9_\-.]+')
MOTIF_PATTERN = re.compile(r'(дыхани|ритм|волна|связк|апекс)', re.I)

PERSONA_ANCHORS = {
    'nia': '#f:liora',
    'veresk': '#f:veresk',
    'guardian': '#f:leya',
}


def extract_patterns(text: str) -> dict:
    text = text or ''
    anchors = ANCHOR_PATTERN.findall(text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    motifs = [line for line in lines if MOTIF_PATTERN.search(line)]
    return {
        'anchors': anchors,
        'motifs': motifs[:20],
        'count': len(motifs),
    }


def stylize(text: str, persona: str, style_hint: dict | None = None) -> str:
    style = style_hint or {}
    opener = style.get('opener', '⟡ шаг')
    closer = style.get('closer', '≈ это не конец')
    return f"{opener}. {text} — {closer}."


class Nia:
    def __init__(self):
        self.mode = 'practical'
        self.guard = Guardian()
        self.modes = load_modes()
        self.persona_override: str | None = None

    def set_mode(self, mode: str):
        if mode in self.modes:
            self.mode = mode

    def set_persona(self, persona: str | None):
        self.persona_override = persona

    def _style_for_persona(self, persona: str) -> dict:
        if persona == 'veresk':
            return self.modes.get('lyrical', {}).get('style', {})
        if persona == 'guardian':
            return self.modes.get('guardian', {}).get('style', {})
        return self.modes.get('practical', {}).get('style', {})

    def reply(self, text: str, facet: str | None = None) -> dict:
        act, msg = self.guard.inspect(text)
        if act:
            return {
                'action': act,
                'message': msg or 'Мягкая пауза. Переформулируем цель.',
                'persona_used': 'guardian',
                'mode': self.mode,
                'anchors': [],
            }

        patterns = extract_patterns(text)
        anchors = set(patterns['anchors'])
        if facet:
            anchors.add(f'#f:{facet}')

        mode_cfg = self.modes.get(self.mode, {})
        persona = self.persona_override or mode_cfg.get('persona', 'nia')

        calibration = auto_analyze([text])
        persona_used = persona
        if persona_used != 'guardian' and (calibration.get('overload') or calibration.get('pressure')):
            persona_used = 'veresk'

        persona_anchor = PERSONA_ANCHORS.get(persona_used)
        if persona_anchor:
            anchors.add(persona_anchor)

        anchors_list = sorted(anchors)
        write_short_term(text=text, tags=['input'], anchors=anchors_list)

        motif_block = ''
        if patterns['count']:
            motif_block = f" Мотивы: {', '.join(patterns['motifs'][:3])}."

        calibration_block = ''
        overload_hits = calibration.get('overload', 0)
        pressure_hits = calibration.get('pressure', 0)
        if overload_hits or pressure_hits:
            signals = []
            if overload_hits:
                signals.append(f'перегруз ×{overload_hits}')
            if pressure_hits:
                signals.append(f'давление ×{pressure_hits}')
            calibration_block = f" Сигналы: {', '.join(signals)}."

        summary = f"Режим: {self.mode}. Грань: {persona_used}.{motif_block}{calibration_block}"
        message = stylize(summary, persona_used, self._style_for_persona(persona_used))
        if anchors_list:
            message = f"{message} {' '.join(anchors_list[:3])}"

        return {
            'action': 'ok',
            'message': message,
            'persona_used': persona_used,
            'mode': self.mode,
            'anchors': anchors_list,
            'motifs': patterns,
            'calibration': calibration,
        }
