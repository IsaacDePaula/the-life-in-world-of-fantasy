# plants.py
from jobs import Plant


PLANTS_IN_WORLD = {
	'elven-high': [
		Plant(
			name_id="nightshade_patch",
			name="Plantação de Nightshade",
			h=4, m=0, d=0,
			items={
				"nightshade": {"min": 1, "max": 5},
			},
		),
		Plant(
			name_id="silverthorn_patch",
			name="Plantação de Silverthorn",
			h=8, m=0, d=0,
			items={
				"silverthorn": {"min": 1, "max": 4},
			},
		),
		Plant(
			name_id="bloodroot_patch",
			name="Plantação de Bloodroot",
			h=5, m=30, d=0,
			items={
				"bloodroot": {"min": 2, "max": 6},
			},
		),
		Plant(
			name_id="dragons_tongue_patch",
			name="Plantação de Língua de Dragão",
			h=10, m=0, d=0,
			items={
				"dragons-tongue": {"min": 1, "max": 3},
			},
		),
		Plant(
			name_id="winters_bite_patch",
			name="Plantação de Mordida do Inverno",
			h=12, m=0, d=0,
			items={
				"winters-bite": {"min": 1, "max": 4},
			},
		),
		Plant(
			name_id="dreamleaf_patch",
			name="Plantação de Folha dos Sonhos",
			h=10, m=30, d=0,
			items={
				"dreamleaf": {"min": 1, "max": 4},
			},
		),
		Plant(
			name_id="bloomlotus_patch",
			name="Plantação de Lótus Florescente",
			h=1, m=0, d=1,
			items={
				"bloomlotus": {"min": 1, "max": 2},
			},
		),
		Plant(
			name_id="firethorn_patch",
			name="Plantação de Espinheiro de Fogo",
			h=14, m=0, d=0,
			items={
				"firethorn": {"min": 1, "max": 3},
			},
		),
		Plant(
			name_id="weavegrass_patch",
			name="Plantação de Grama Tecelã",
			h=6, m=0, d=0,
			items={
				"weavegrass": {"min": 2, "max": 6},
			},
		),
		Plant(
			name_id="liferoot_patch",
			name="Plantação de Raiz da Vida",
			h=8, m=0, d=0,
			items={
				"liferoot": {"min": 1, "max": 5},
			},
		),
		Plant(
			name_id="starbloom_patch",
			name="Plantação de Flor Estelar",
			h=18, m=0, d=0,
			items={
				"starbloom": {"min": 1, "max": 3},
			},
		),
		Plant(
			name_id="rotshroom_patch",
			name="Cultivo de Cogumelo da Podridão",
			h=20, m=0, d=0,
			items={
				"rotshroom": {"min": 1, "max": 3},
			},
		),
		Plant(
			name_id="mindthorn_patch",
			name="Plantação de Espinheiro Mental",
			h=16, m=0, d=0,
			items={
				"mindthorn": {"min": 1, "max": 3},
			},
		),
		Plant(
			name_id="gravedust_patch",
			name="Fonte de Pó da Sepultura",
			h=24, m=0, d=0,
			items={
				"gravedust": {"min": 1, "max": 3},
			},
		),
		Plant(
			name_id="zapthistle_patch",
			name="Plantação de Cardo Elétrico",
			h=12, m=0, d=0,
			items={
				"zapthistle": {"min": 1, "max": 4},
			},
		),
		Plant(
			name_id="sirens_call_patch",
			name="Plantação de Chamado da Sereia",
			h=18, m=0, d=0,
			items={
				"sirens-call": {"min": 1, "max": 3},
			},
		),
		Plant(
			name_id="deaths_beckon_patch",
			name="Plantação de Chamado da Morte",
			h=24, m=0, d=0,
			items={
				"deaths-beckon": {"min": 1, "max": 2},
			},
		),
		Plant(
			name_id="shadowleaf_patch",
			name="Plantação de Folha das Sombras",
			h=20, m=0, d=0,
			items={
				"shadowleaf": {"min": 1, "max": 3},
			},
		),
		Plant(
			name_id="cinderroot_patch",
			name="Plantação de Raiz de Brasa",
			h=12, m=0, d=0,
			items={
				"cinderroot": {"min": 1, "max": 4},
			},
		),
		Plant(
			name_id="graveflower_patch",
			name="Plantação de Flor da Sepultura",
			h=2, m=0, d=1,
			items={
				"graveflower": {"min": 1, "max": 2},
			},
		),
	],
}