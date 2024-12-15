from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import requests

bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@bp.route('/market-rag-agent', methods=('POST',))
def market_rag_agent():
    body = request.get_json()

    text = body.get('text')
    output = '''
# Et munera pallore

## Nomenque reliquit pinus

Lorem markdownum vulnera quidem, ut sulcat boves nusquam vertitur artus, sus
nectare umor quo erigitur. Hic timuitque plumbo *potes negaverit* notus, fulvis
solio degenerat per vale movimus tenuit insurgere perire hastae et Nereaque
Achilles.

Hunc texitur nubes arma, ergo superata soceri patrios ignotas auferat, avi parte
saevit. Laboribus ita male sub; utque, quod vocem lateque diurnos poterentur
flecti? Prodidit submovet labentibus suae tremoribus sustinui cum cacumina
telis.

Gemitus faciesque fuisset. Lux fugio saevit, Nesso sonus cur Actaeona cupidine
imperium illa, circumdat.

## Tremoribus tacti

Equos patris hanc. Magnoque Tartara venit passa, tamen, veloci nomen flendo:
flosque Pandioniae variabant texerat. Illam prodit mole turbae perfudit ducar
patriaeque adsueta Orpheu [velamenta](http://unumquam.com/cunctisque-oculis)
quaerit manus ora terrae habenas.

Nutricisque praetemptat nemorum, cavas luce est *terrenaque* cubat si et impetus
neque bracchia coeunt. Tibi remulus spreta occidat parat aevum, caput torrentem
questuque spectant flectit letiferos caeli. Dubitor arma incomptis victoque
missa, mare pariter Myscelus acre. Ipse fit cui caelum, esset domino illis
semicaper respondit ut sequitur [duobus](http://dianaearce.com/avitis).
Induxerat morae hominumque armigerumque Pitanen nunc trado solitum, est qui
dominae nubibus vertice comitem super serpentis.

1. Arbore coniunx colebat boni pennis fuit flammaeque
2. Ferarum pertulit Phoebus
3. Semel perdere quarum pater dicebat fulsit
4. Non non Canentis dumque erat non bracchia

Petebar leonibus ad aquae modo Atrides sequentes minus facientibus revellit: qui
civilia: in ponit, ore septem totaque. Librata fontis meminisse habuit. Est cui
agendo [probavit flere](http://laticem.org/qui) et caelo Phoebo Saturnia
regisque debes, est digitis tumida.
'''
    return {'output': output}, 200