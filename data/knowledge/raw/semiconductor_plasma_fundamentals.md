# 반도체 장비와 플라즈마

## 반도체 공정에서 플라즈마의 역할

반도체 제조에서 플라즈마는 patterning, sputtering, etching, deposition, dry cleaning 등 다양한 공정에 활용된다. 플라즈마는 가스에 에너지를 공급하여 전자, 이온, 라디칼, 여기종을 생성하고, 이들이 웨이퍼 표면과 반응하면서 박막을 제거하거나 증착하거나 표면을 개질한다.

식각 공정에서는 이온의 물리적 충돌과 라디칼의 화학 반응이 함께 작용한다. 이온은 표면 방향으로 가속되어 물리적 에너지를 전달하고, 라디칼은 표면 물질과 반응하여 휘발성 생성물을 만든다. 따라서 식각 결과는 단순히 장비 외형이나 입력 recipe만으로 결정되지 않고, 장비 내부에서 형성되는 플라즈마 상태와 표면 반응의 조합에 의해 결정된다.

같은 부품과 같은 장비를 사용하고 외부 공정 조건이 같아 보여도 결과가 달라질 수 있다. 이는 플라즈마가 장비 내부 상태, gas mixture, pressure, source_power, bias_power, 온도, 표면 상태, cleanroom 상태, 유지보수 이력 등에 민감하게 반응하기 때문이다. 플라즈마 공정은 입력 조건이 플라즈마 파라미터를 만들고, 플라즈마 파라미터가 표면 반응을 변화시키며, 최종적으로 etch rate, selectivity, uniformity, feature profile, critical dimension 같은 품질 지표로 이어지는 복합 시스템이다.

## 플라즈마의 정의와 기본 특성

플라즈마는 고체, 액체, 기체에 이어 물질의 네 번째 상태로 불린다. 가스가 충분한 에너지를 받아 부분적으로 또는 전체적으로 이온화되면 중성 입자, 전자, 이온이 함께 존재하는 상태가 된다. 멀리서 보면 전체적으로 전기적 중성을 유지하지만, 가까이서 보면 전자와 이온이 전기력으로 상호작용한다. 이 때문에 플라즈마는 전기적 성질을 지닌 유체로 이해할 수 있다.

플라즈마는 charged particle과 neutral particle이 함께 존재하는 quasi-neutral gas이며, 개별 입자의 운동만으로 설명되지 않고 집단적 거동을 보인다. 여기서 quasi-neutral은 플라즈마 중심부에서 전자 밀도와 이온 밀도가 거의 같아 전체적으로 전기적 중성을 유지한다는 뜻이다. collective behavior는 많은 입자가 전기장과 자기장에 의해 서로 영향을 주며 집단적으로 움직이는 특성을 의미한다.

플라즈마의 관심 영역은 충분한 수의 전자와 이온이 존재해 안정적으로 방전이 유지되는 상태이다. 단일 입자 충돌이나 순간적인 방전보다, 다수의 하전 입자가 존재하여 전기장, 자기장, 충돌, 확산, 벽 손실 등이 함께 작용하는 상태가 반도체 플라즈마 공정에서 중요하다.

## 플라즈마 생성 원리

상온의 일반적인 기체는 대부분 중성 상태로 존재하므로, 플라즈마를 만들기 위해서는 추가적인 전자와 이온이 필요하다. 전자와 이온은 열에너지, 전기에너지, 충돌에너지 등을 통해 생성될 수 있다. 반도체 장비에서는 주로 전기장을 이용해 전자를 가열하고, 고에너지 전자가 중성종과 충돌하여 이온화 반응을 일으키는 방식으로 플라즈마를 발생시킨다.

전기장이 전자에 힘을 가하면 전자는 가속된다. 가속된 전자가 충분히 높은 에너지를 얻으면 중성종과 충돌하여 전자를 떼어내고, 그 결과 양이온과 새로운 전자가 생성된다. 이 과정이 반복되면 전자의 수가 증가하고 이온화가 연쇄적으로 일어나 플라즈마가 유지된다.

전자와 이온은 질량 차이가 매우 크다. 전자는 이온보다 훨씬 가볍기 때문에 같은 에너지를 받더라도 훨씬 빠르게 움직인다. 이 때문에 전자는 에너지를 빠르게 얻고 중성종을 이온화하는 주된 역할을 하며, 이온은 상대적으로 무겁고 느리지만 sheath 전기장에 의해 가속되어 표면 충돌과 식각에 큰 영향을 준다.

플라즈마 생성에는 전자 충돌 이온화가 핵심적이다. 빠른 전자가 원자 또는 분자와 충돌하면 탄성 충돌, 여기, 이온화, 해리, 재결합, 부착 같은 다양한 반응이 발생한다. 이 중 이온화는 중성종에서 전자를 떼어내 양이온과 추가 전자를 만드는 반응이며, 플라즈마 밀도 증가에 직접적으로 기여한다.

## Townsend 방전과 점화 조건

플라즈마가 안정적으로 발생하려면 전자가 충분히 가속되어 중성종과 충돌하고, 그 충돌이 다시 새로운 전자를 만들어야 한다. Townsend 방전은 전자 avalanche를 설명하는 개념이다. 전자가 전기장에 의해 가속되어 중성종을 이온화하고, 새로 생긴 전자가 다시 이온화를 반복하면서 전류가 급격히 증가한다.

Townsend ionization coefficient는 전자가 이동하는 동안 단위 길이당 얼마나 많은 이온화 반응이 발생하는지를 나타낸다. Townsend secondary electron emission coefficient는 이온이 전극이나 벽에 충돌했을 때 표면에서 방출되는 2차 전자의 정도를 나타낸다. 이 두 과정이 충분히 결합되면 외부에서 계속 전자를 공급하지 않아도 방전이 유지된다.

Paschen curve는 방전 개시 전압이 pressure와 전극 간 거리의 곱에 따라 어떻게 달라지는지를 보여준다. pressure가 너무 낮으면 전자가 중성종과 충돌할 기회가 부족하고, 전극 간 거리가 너무 짧아도 충분한 충돌 연쇄가 일어나기 어렵다. 반대로 pressure가 너무 높으면 전자가 잦은 충돌로 충분히 가속되지 못하고, 전극 간 거리가 너무 길면 필요한 전압이 증가할 수 있다. 따라서 플라즈마 ignition에는 적절한 pressure와 전극 간 거리가 필요하다.

RF 방전에서는 전기장의 방향이 시간에 따라 바뀌므로 전자가 단순히 한 방향으로만 가속되는 DC 방전과 다르게 움직인다. RF field에서는 전자가 왕복 운동하며 에너지를 얻고, 이 과정에서 전자 모드와 축적 효과가 나타나 DC Paschen curve와 다른 ignition 특성을 보일 수 있다.

## Plasma Source 개요

플라즈마 source는 전기장을 만들어 전자를 가열하고, 이 전자가 중성종을 이온화하도록 하는 장치 구조이다. 대표적인 source로는 CCP와 ICP가 있다. CCP는 전극 사이의 전위차를 이용해 전기장을 만들고, ICP는 시간에 따라 변하는 자기장을 이용해 유도 전기장을 만든다.

Gauss 법칙과 Poisson 방정식은 전하 분포와 전기장, 전위 사이의 관계를 설명한다. 전하가 공간에 분포하면 전기장이 생기고, 전기장은 전위의 공간적 변화로 표현된다. CCP에서는 전극 사이에 형성되는 전기장이 플라즈마 생성과 sheath 형성에 직접적으로 관여한다.

Ampere 법칙과 Faraday 법칙은 전류, 자기장, 유도 전기장 사이의 관계를 설명한다. 전류가 흐르면 자기장이 생기고, 시간에 따라 변하는 자기장은 다시 전기장을 유도한다. ICP에서는 코일 전류가 시간적으로 변하는 자기장을 만들고, 이 자기장이 플라즈마 내부에 원형의 유도 전기장을 만들어 전자를 가열한다.

## CCP의 특성

CCP는 Capacitively Coupled Plasma의 약자로, 전극과 전극 사이에 형성되는 전기장을 이용해 플라즈마를 생성한다. 전기장이 벽과 벽 사이에 형성되기 때문에 하전 입자가 전극이나 벽으로 충돌하기 쉽다. 이 과정에서 하전 입자 손실, sheath 형성, 이온의 벽 충돌, 표면 식각 및 damage가 함께 나타난다.

CCP에서는 전극 주변에 sheath가 형성된다. 플라즈마 중심부에서는 전자 밀도와 이온 밀도가 거의 같지만, 벽 근처에서는 전자가 빠르게 벽으로 손실되기 때문에 전하 균형이 깨진다. 전자는 이온보다 훨씬 빠르게 움직이므로 벽은 음전하를 띠게 되고, 이로 인해 벽 근처에 전기장이 형성된다. 이 전기장은 양이온을 벽 또는 웨이퍼 방향으로 가속한다.

CCP의 장점은 구조가 비교적 단순하고, 전극에 인가되는 전압으로 이온 에너지를 직접적으로 제어하기 쉽다는 점이다. 반면 플라즈마 밀도와 이온 에너지를 독립적으로 제어하기 어렵고, 높은 이온 에너지로 인해 damage가 발생할 수 있다.

## Sheath와 ion_energy

Sheath는 플라즈마와 벽 또는 전극 사이에 형성되는 전하 불균형 영역이다. 플라즈마 중심부에서는 quasi-neutral 상태가 유지되지만, 벽 근처에서는 전자가 먼저 빠져나가고 이온이 상대적으로 남게 된다. 그 결과 전위차가 생기며, 이 전위차가 이온을 웨이퍼 방향으로 가속한다.

ion_energy는 이온이 표면에 도달할 때 갖는 평균 에너지와 관련된다. ion_energy가 높으면 물리적 식각 성분이 강해지고 anisotropic etching에 유리할 수 있지만, 지나치게 높으면 mask 손상, 기판 damage, charging damage, profile distortion이 발생할 수 있다. 반대로 ion_energy가 너무 낮으면 표면 반응을 활성화하거나 방향성 있는 식각을 유도하기 어렵다.

Sheath는 etching과 damage를 동시에 결정하는 핵심 영역이다. 식각 공정에서 이온이 표면에 수직에 가깝게 입사하면 높은 aspect ratio 구조를 형성하는 데 유리하다. 그러나 sheath 전기장, ion energy distribution, ion angular distribution이 불안정하면 식각 profile이 왜곡될 수 있다.

## ICP의 특성

ICP는 Inductively Coupled Plasma의 약자로, 코일에 흐르는 RF 전류가 시간적으로 변하는 자기장을 만들고, 그 자기장이 플라즈마 내부에 유도 전기장을 형성하여 전자를 가열한다. ICP의 전기장은 원형으로 형성되기 때문에 하전 입자가 내부에서 순환하며 에너지를 얻을 수 있다.

ICP는 벽과 벽 사이의 직선 전기장을 이용하는 CCP에 비해 하전 입자의 벽 손실이 상대적으로 적고, 벽 근처 전기장이 낮으며, 이온의 벽 충돌이 줄어드는 장점이 있다. 이 때문에 ICP는 낮은 pressure에서도 높은 플라즈마 밀도를 얻을 수 있고, high density plasma source로 널리 사용된다.

ICP에서 source_power는 주로 플라즈마 생성과 밀도 증가에 관여한다. source_power가 증가하면 전자 가열이 강해지고 이온화 반응이 증가하여 plasma density와 ion_flux가 증가할 수 있다. 그러나 밀도는 무한정 증가하지 않으며, 전력 흡수 구조, skin depth, capacitive coupling, 손실 메커니즘에 의해 제한된다.

ICP에서는 플라즈마 생성과 이온 가속을 분리하기 위해 별도의 bias 회로를 사용하는 경우가 많다. Bias ICP에서는 source_power가 주로 plasma density와 ion_flux를 조절하고, bias_power가 sheath 전압과 ion_energy를 조절한다. 따라서 ion_flux와 ion_energy를 비교적 독립적으로 제어할 수 있어 식각 공정 최적화에 유리하다.

## 공정 파라미터와 플라즈마 특성

반도체 플라즈마 공정에서 중요한 입력 파라미터는 pressure, gas flow, gas mixture, source_power, bias_power, source frequency, RF frequency, chamber structure, temperature 등이다. 이 값들은 플라즈마 내부의 electron density, electron temperature, ion_flux, ion_energy, radical density, plasma potential, sheath 특성을 변화시킨다.

pressure는 입자 충돌 빈도와 평균 자유 행로를 결정한다. pressure가 낮으면 입자들이 충돌하기 전 더 긴 거리를 이동할 수 있어 방향성이 좋아질 수 있지만, 이온화 충돌이 부족하면 플라즈마 유지가 어려울 수 있다. pressure가 높으면 충돌이 증가하여 라디칼 생성이나 반응 빈도는 증가할 수 있지만, 이온의 방향성이 감소하고 ion energy distribution이 변할 수 있다.

source_power는 전자 가열과 이온화 반응에 영향을 준다. 일반적으로 source_power가 증가하면 plasma density가 증가하고, 그 결과 ion_flux가 증가할 수 있다. ion_flux가 증가하면 웨이퍼 표면에 도달하는 이온 수가 많아져 식각 속도에 영향을 준다.

bias_power는 sheath 전압과 이온 가속에 영향을 준다. bias_power가 증가하면 웨이퍼로 입사하는 이온의 ion_energy가 증가하는 경향이 있다. 이는 방향성 식각에는 유리하지만, 과도한 bias_power는 표면 damage와 mask erosion을 증가시킬 수 있다.

gas mixture는 생성되는 라디칼과 이온 종을 결정한다. 예를 들어 Ar은 물리적 충돌과 플라즈마 안정화에 자주 활용되고, CF4나 O2 계열 가스는 F radical, O radical, CFx species 등을 만들어 Si, SiO2, polymer 형성 및 제거에 영향을 준다.

## Plasma Chemistry 기본 반응

플라즈마 chemistry는 전자, 이온, 라디칼, 중성종, 여기종이 충돌하고 반응하는 과정을 다룬다. 빠른 전자가 원자나 분자와 충돌하면 여러 종류의 반응이 발생한다.

탄성 충돌은 전자가 중성종과 충돌하지만 내부 에너지 상태를 크게 바꾸지 않는 반응이다. 여기 반응은 전자가 중성종에 에너지를 전달하여 원자나 분자를 높은 에너지 상태로 올리는 반응이다. 여기된 입자는 다시 안정한 상태로 내려오면서 특정 파장의 빛을 방출할 수 있다. 이 빛은 OES 진단의 근거가 된다.

이온화 반응은 전자가 중성종과 충돌하여 전자를 하나 더 떼어내고 양이온과 추가 전자를 만드는 과정이다. 해리 반응은 분자가 전자 충돌에 의해 여러 조각으로 나뉘는 과정이며, 식각 공정에서 라디칼 생성에 중요하다. 재결합은 전자와 이온이 결합하여 중성종이 되는 과정이고, 부착은 전자가 중성종에 붙어 음이온을 만드는 과정이다.

Ar plasma에서는 전자가 Ar과 충돌하여 Ar을 여기시키거나 Ar+로 이온화한다. Ar의 직접 이온화에는 비교적 높은 전자 에너지가 필요하지만, Ar*와 같은 여기종을 거치면 추가 에너지만으로 이온화가 진행될 수 있다. 따라서 전자 에너지 분포와 metastable species의 존재는 전체 이온화 효율에 영향을 준다.

CF4와 O2를 포함하는 플라즈마에서는 전자 충돌에 의해 CFx, F, O 등 다양한 라디칼과 이온이 생성된다. 이들 species는 표면에서 화학 반응을 일으켜 휘발성 생성물을 만들거나 polymer passivation을 형성한다. 따라서 plasma chemistry는 etch rate, selectivity, profile control에 직접적인 영향을 준다.

## 고온 플라즈마와 저온 플라즈마

고온 플라즈마는 이온화율이 매우 높고, 중성종 밀도보다 이온과 전자의 밀도가 큰 상태에 가깝다. 이 경우 전자, 이온, 중성종의 온도가 서로 비슷해질 수 있다. 핵융합 플라즈마와 같은 고온 플라즈마가 여기에 해당한다.

반도체 공정에서 주로 사용하는 플라즈마는 저온 플라즈마이다. 저온 플라즈마는 이온화율이 매우 낮아 중성종 밀도가 이온과 전자 밀도보다 훨씬 크다. 또한 전자 온도는 높지만 이온 온도와 가스 온도는 상대적으로 낮다. 이 특성 덕분에 전체 gas 온도를 매우 높이지 않고도 전자 충돌 반응을 통해 화학적으로 활성이 높은 species를 생성할 수 있다.

저온 플라즈마에서는 electron temperature와 gas temperature가 다르기 때문에 비평형 특성이 중요하다. 전자는 높은 에너지로 이온화와 여기 반응을 일으키고, 이온과 중성종은 상대적으로 낮은 온도로 공정 표면에 도달한다. 이 비평형성이 반도체 공정에서 플라즈마를 유용하게 만드는 핵심이다.

## 전자에너지분포와 반응 선택성

전자에너지분포는 플라즈마 내 전자들이 어떤 에너지 범위에 얼마나 분포하는지를 나타낸다. 전자에너지분포는 excitation, ionization, dissociation 같은 반응의 발생 확률을 결정한다. 특정 반응은 일정 에너지 이상의 전자가 필요하므로, 평균 전자 온도뿐만 아니라 고에너지 꼬리 부분의 전자 비율도 중요하다.

전자에너지분포에서 낮은 에너지 영역은 탄성 충돌과 일부 여기 반응에 영향을 주고, 높은 에너지 영역은 이온화와 해리 반응에 크게 관여한다. 따라서 source_power, pressure, gas mixture, EEPF 또는 EEDF 형태가 달라지면 같은 가스라도 생성되는 species와 반응 경로가 달라질 수 있다.

반도체 플라즈마 공정에서는 단순히 많은 플라즈마를 만드는 것보다 원하는 반응을 선택적으로 유도하는 것이 중요하다. 예를 들어 식각에 필요한 라디칼을 충분히 만들면서도 과도한 ion_energy로 인한 damage를 줄이는 균형이 필요하다.

## Plasma Diagnostics 개요

Plasma Diagnostics는 장비 내부에서 실제로 어떤 플라즈마 상태가 형성되었는지를 측정하거나 추정하는 방법이다. 같은 장비와 같은 recipe라도 플라즈마 상태가 다를 수 있기 때문에, 진단은 공정 결과 차이를 해석하고 모델을 검증하는 데 필수적이다.

진단 대상에는 electron density, electron temperature, ion_flux, ion_energy, radical density, neutral density, plasma potential, sheath 특성, gas composition, exhaust species 등이 포함된다. 진단 방법은 측정 대상과 위치에 따라 probe method, electromagnetic field method, optical emission spectroscopy, laser spectroscopy, mass spectroscopy, ion energy analyzer 등으로 나뉜다.

Probe type sensor는 plasma parameters를 직접 측정하는 데 사용될 수 있다. V-I probe는 RF power 상태 확인에 활용될 수 있고, OES는 chemical state를 파악하는 데 활용된다. SP-OES 또는 RGA는 exhaust gas 분석에 사용될 수 있다.

## Langmuir Probe

Langmuir Probe는 플라즈마에 금속 tip을 삽입하고, tip에 인가한 전압에 대해 흐르는 전류를 측정하여 plasma parameter를 추정하는 방법이다. 전압-전류 특성을 분석하면 electron density, electron temperature, plasma potential, floating potential, EEDF 등을 얻을 수 있다.

Langmuir Probe의 장점은 다양한 플라즈마 변수를 직접 측정할 수 있고, 적절히 사용하면 정밀한 측정이 가능하다는 점이다. 특히 EEDF 측정을 통해 전자의 가열 특성을 관찰할 수 있다.

단점은 probe가 플라즈마에 직접 삽입되므로 플라즈마를 교란할 수 있다는 점이다. Probe가 전자 전류를 끌어내기 때문에 충분한 접지 면적이 필요하며, probe로 빠져나간 전류가 플라즈마 상태에 큰 영향을 주지 않아야 한다. 또한 tip이 공정 gas와 반응하거나 증착·식각되면 측정 신뢰도가 떨어진다. 실제 반도체 공정 gas 환경에서는 tip 오염과 부식 때문에 사용이 어려운 경우가 많다.

## Floating Harmonics Probe와 Cutoff Probe

Floating Harmonics Probe는 플라즈마에 직접 큰 전류를 뽑아내지 않고, floating 상태에서 발생하는 harmonic 성분을 이용해 electron temperature와 electron density를 추정하는 방법이다. 공정 환경에서 Langmuir Probe보다 교란이 적은 방식으로 활용될 수 있다.

Cutoff Probe는 플라즈마의 전자 밀도와 cutoff frequency 사이의 관계를 이용한다. 전자 밀도가 높을수록 플라즈마가 통과시키거나 차단하는 전자기파 주파수 조건이 달라진다. 따라서 cutoff frequency를 측정하면 electron density를 추정할 수 있다.

## OES와 광학 진단

OES는 Optical Emission Spectroscopy의 약자이다. 플라즈마에서 여기된 원자나 분자가 안정한 상태로 돌아오면서 고유한 파장의 빛을 방출한다. 이 빛의 파장과 세기를 분석하면 플라즈마 내 species 종류, 에너지 상태, 상대적 밀도 변화를 파악할 수 있다.

OES의 장점은 비접촉식 진단이라는 점이다. 플라즈마에 probe를 삽입하지 않아 공정을 교란하지 않고, 실시간으로 특정 species 변화를 관찰할 수 있다. 다만 방출광 세기는 electron impact excitation, species density, optical path, 장비 구조의 영향을 함께 받으므로 정량 해석에는 주의가 필요하다.

Laser spectroscopy는 특정 species의 흡수나 형광을 이용해 radical, neutral, ion 등의 밀도나 온도 정보를 얻는 방법이다. Mass spectroscopy는 이온 또는 중성종의 질량을 분석하여 gas composition과 reaction product를 파악하는 데 사용된다. Ion energy analyzer는 웨이퍼에 도달하는 이온의 에너지 분포를 분석하는 데 활용된다.

## SP-OES와 End Point Detection

SP-OES는 Self Plasma OES의 개념으로, 플라즈마가 거의 발생하지 않는 exhaust 부근에서 gas를 채취한 뒤 별도의 미약한 플라즈마를 만들어 빛을 분석하는 방식이다. Exhaust 부근에서는 자연 방출광이 약해 직접 OES 분석이 어려울 수 있으므로, 채취한 gas를 자체적으로 여기시켜 분석한다.

SP-OES는 exhaust gas 분석뿐 아니라 EPD, 즉 End Point Detection에도 활용될 수 있다. 예를 들어 cleaning 반응에서 Si가 F와 반응하여 SiF4를 만들 때, cleaning이 진행 중일 때와 종료 시점에서 SiF4 검출량이 달라질 수 있다. 특정 반응 생성물의 농도 변화가 급격히 나타나는 시점을 이용하면 cleaning 종료 시점을 예측하고 공정 시간을 효율적으로 제어할 수 있다.

## Plasma Simulation의 필요성

플라즈마 장비 내부의 물리적 현상을 모두 직접 진단하기는 어렵다. 특히 고온, 저압, RF 전력, 복잡한 gas chemistry, sheath, 표면 반응이 동시에 작용하는 환경에서는 실험만으로 모든 변수를 파악하기 어렵다. 시행착오 방식은 많은 시간과 비용, 인적 자원을 필요로 한다.

Plasma Simulation은 진단하기 어려운 플라즈마 변수를 예측하고, 장비 내부에서 발생하는 물리·화학적 현상을 이해하기 위해 사용된다. 시뮬레이션을 통해 electron density, electron temperature, plasma potential, ion_flux, ion_energy, radical density, gas temperature, surface reaction rate 등을 계산할 수 있다. 이는 제품 개발 시간을 줄이고 공정 조건 최적화에 도움을 준다.

Plasma Simulation은 Maxwell 방정식, Boltzmann 방정식, 유체 방정식, 입자 운동 방정식, plasma chemistry, surface reaction 등을 조합하여 구성된다. 다만 모든 상황에 완벽하게 적용 가능한 일반 프로그램은 현실적으로 어렵다. 각 상황에 맞는 모델식을 세우고, 그 모델의 의미와 한계를 이해한 상태에서 사용해야 한다.

## Plasma Simulation의 한계와 모델 선택

Plasma Simulation은 수치적 오차와 모델 가정을 포함한다. 입력 데이터베이스, 반응 계수, 표면 반응 모델, boundary condition, external circuit 모델, chamber geometry, mesh, time step 등에 따라 결과가 달라질 수 있다. 따라서 시뮬레이션 결과는 절대적인 정답이 아니라, 실험과 진단으로 검증하면서 사용하는 해석 도구로 이해해야 한다.

모델 선택은 계산 목적과 물리적 scale에 따라 달라진다. 모든 입자를 자세히 추적하면 정확한 물리 정보를 얻을 수 있지만 계산량이 매우 크다. 반대로 평균화된 유체 모델을 사용하면 계산은 빠르지만 많은 가정이 필요하다. 따라서 실제 공정 분석에서는 particle simulation, kinetic simulation, fluid simulation, global model, surface model을 목적에 맞게 조합한다.

Knudsen number는 continuum model을 사용할 수 있는지 판단하는 기준 중 하나이다. Knudsen number가 매우 작으면 유체 연속체 가정이 잘 맞고, Navier-Stokes 계열의 모델을 사용할 수 있다. Knudsen number가 커지면 slip flow, transition regime, free molecular regime으로 이동하며 연속체 가정이 약해진다. 플라즈마 공정에서도 압력과 characteristic length에 따라 적절한 모델 선택이 필요하다.

## Fluid Simulation

Fluid Simulation은 입자들의 분포함수를 속도 공간에서 평균하여 밀도, 평균 속도, 온도 같은 거시적 변수로 플라즈마를 설명한다. 주로 continuity equation, momentum conservation, drift-diffusion approximation, energy conservation을 사용한다.

Fluid Simulation은 계산이 상대적으로 쉽고 복잡한 chemistry를 포함하기 유리하다. 많은 species와 반응을 포함해야 하는 반도체 공정에서는 유체 모델이 실용적이다. 그러나 속도 분포를 평균화하기 때문에 비평형적 입자 거동이나 고에너지 tail, sheath 내부의 세부 운동을 정확히 표현하기 어려울 수 있다.

Fluid Simulation 도구로는 CFD-ACE+, COMSOL Multiphysics, Quantemol-VT, VizGlow 등이 활용될 수 있다. 이러한 도구는 장비 구조, 전자기장, gas flow, plasma chemistry, surface reaction을 결합해 장비 내부의 플라즈마 상태를 해석하는 데 사용된다.

## Particle Simulation과 Kinetic Simulation

Particle Simulation은 super-particle을 사용하여 다수의 실제 입자를 대표하게 하고, 각 입자의 운동을 Newton-Lorentz 방정식으로 추적한다. 전기장과 자기장이 입자에 힘을 가하고, 입자의 분포가 다시 전하 밀도와 전위를 만든다. Poisson 방정식은 전하 분포와 전위의 관계를 계산하는 데 사용된다.

Particle Simulation은 가정이 상대적으로 적고 입자 수준의 물리 현상을 잘 표현할 수 있지만 계산량이 크다. 특히 2D 또는 3D 장비 전체를 해석하거나 많은 충돌과 chemistry를 포함하려면 매우 큰 계산 자원이 필요하다.

Kinetic Simulation은 분포함수를 직접 다루며 Boltzmann 방정식을 푼다. 이는 입자의 위치와 속도 분포를 더 자세히 표현할 수 있으나 계산 부담이 크다. Kinetic model은 EEDF, non-local electron kinetics, sheath physics, collisionless heating 같은 세부 물리 이해에 유용하다.

## 공정 해석에서의 시뮬레이션 활용

플라즈마 시뮬레이션은 공정 recipe 변화가 플라즈마 상태에 어떤 영향을 주는지 이해하는 데 사용된다. 예를 들어 pressure를 바꾸면 충돌 빈도와 ion energy distribution이 달라지고, source_power를 바꾸면 plasma density와 ion_flux가 변하며, bias_power를 바꾸면 sheath 전압과 ion_energy가 변한다.

VizGlow 같은 유체 기반 시뮬레이션은 코로나 방전, CCP reactor, dusty plasma dynamics 같은 문제에 활용될 수 있다. Dusty plasma에서는 dust particle이 electric field, ion drag, gravity, Coulomb force의 영향을 받아 sheath edge 근처에서 진동하거나 포획될 수 있다.

K-PIC 같은 particle-in-cell 기반 시뮬레이션은 CCP에서 electron transport와 electron heating을 분석하는 데 사용될 수 있다. 전극 반지름, pressure, RF frequency, dielectric constant, secondary electron emission coefficient 같은 조건을 바꿔 time-averaged electron temperature, plasma potential, electron density의 공간 분포를 계산할 수 있다.

K-SPEED와 K-0DPlasma 같은 도구는 특정 공정 또는 장비 조건에서 플라즈마 특성을 빠르게 예측하고 실험 결과와 비교하는 데 활용될 수 있다. 이러한 도구는 RAG 기반 AI 플랫폼에서 플라즈마 모델링 개념, 공정 파라미터 영향, 시뮬레이션 결과 해석을 설명하는 지식 소스로 사용할 수 있다.

## RAG 지식베이스 활용 관점

이 문서는 반도체 플라즈마 공정의 기본 개념, 플라즈마 생성 원리, CCP와 ICP의 차이, sheath와 ion_energy, source_power와 bias_power의 역할, pressure와 gas chemistry의 영향, plasma diagnostics, plasma simulation의 필요성과 한계를 설명하는 지식베이스로 활용할 수 있다.

질의응답 시스템에서는 사용자가 “플라즈마가 무엇인가”, “ICP와 CCP의 차이는 무엇인가”, “source_power와 bias_power는 각각 무엇을 조절하는가”, “pressure가 식각에 어떤 영향을 주는가”, “ion_flux와 ion_energy는 왜 중요한가”, “Langmuir Probe와 OES는 무엇을 측정하는가”, “플라즈마 시뮬레이션은 왜 필요한가”와 같은 질문을 할 때 이 문서를 근거로 답변할 수 있다.

AI 기반 플라즈마 식각 플랫폼에서는 이 문서를 개념 설명용 RAG 자료로 사용하고, 별도의 시뮬레이터 매뉴얼이나 논문 자료와 함께 연결하면 좋다. 예측 모델이 산출한 ion_flux, ion_energy, etch_score를 설명할 때도 이 문서의 플라즈마 물리와 공정 파라미터 설명을 활용할 수 있다.
