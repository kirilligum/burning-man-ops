# Workbook Coverage

This file accounts for the operational content in
`Treble Makers Checklists - 2026.ods`. The workbook remains source evidence;
canonical procedures are the XML files under `data/tasks/` and `data/items/`.

Coverage is by logical source instruction rather than by copying every cell.
Several workbook rows describe one outcome and therefore map to one task. A
repeated row maps to the same task instead of creating a conflicting duplicate.

## Coverage meanings

- **Expanded** — one or more canonical tasks cover the operational outcome.
- **Runtime** — the value belongs in an on-playa roster, map, assignment sheet,
  issue log, or approved external account and is not stored in repository XML.
- **Excluded** — the source is non-operational, protected, deprecated,
  duplicated, explicitly out of date, or too ambiguous to use safely.
- **Field detail required** — the work package exists, but the responsible lead
  must supply actual equipment geometry, identifiers, values, or instructions
  before field use.

## Dominatrix checklists

The Morning and Evening Dominatrix sheets substantially duplicate each other.
They share these canonical outcomes.

| Source instruction | Coverage | Canonical task or decision |
| --- | --- | --- |
| Receive prior-shift briefing | Expanded | `Begin_Dominatrix_shift` |
| Know current medical and Ranger locations | Expanded | `Begin_Dominatrix_shift` uses the 2026 city plan |
| Locate fire blankets, extinguishers, first-aid kits, and naloxone | Expanded | `Begin_Dominatrix_shift` |
| Monitor fresh water and gray water | Expanded | `Read_fresh_water_tank_level`; `Inspect_gray-water_IBC` |
| Monitor generator fuel every two hours | Expanded | `Read_generator_fuel_level` reports every exact reading |
| Hail water, gray-water, toilet, RV, or fuel service | Expanded | `Coordinate_camp_service_visit`; `Coordinate_generator_refueling` |
| Find vouchers, money, provider details, or RV servicing records | Runtime | Supplied by the Dominatrix; protected payment, contact, and private RV data are excluded |
| Close showers and prioritize drinking water when supply is low | Expanded | `Protect_drinking_water_supply` |
| Ensure the camp sink works and is clean | Expanded | `Inspect_and_clean_camp_sink` |
| Ensure cleaning supplies are available | Expanded | `Inspect_camp_cleaning_supplies` |
| Verify and welcome new arrivals | Expanded | `Welcome_new_camp_arrival`; roster contents remain runtime data |
| Issue wristband or optional necklace | Expanded | `Welcome_new_camp_arrival` |
| Give the camp tour and keep service lanes clear | Expanded | `Welcome_new_camp_arrival` |
| Staff, brief, and review every scheduled shift | Expanded | `Coordinate_camp_shift` |
| Add checklist instructions during a shift | Expanded with correction | `Hand_off_Dominatrix_shift` records proposals in `Camp_Issue_Log`; controlled cards are not edited on playa |
| Brief the next Dominatrix | Expanded | `Hand_off_Dominatrix_shift` |
| Motivational whip or persona text | Excluded | Camp tone, not an observable operating outcome |

The source uses conflicting generator escalation thresholds: below one-half,
below two-thirds, and below 70 percent. `Read_generator_fuel_level` therefore
reports every exact reading until the Fuel Lead approves one threshold.

## Morning checklist

| Rows | Source area or instruction | Canonical coverage |
| --- | --- | --- |
| 3–4 | Kitchen tables and cooking surfaces | `Clean_communal_kitchen_tables`; `Clean_communal_kitchen_cooking_surfaces` |
| 5–6 | Dry and wet kitchen trash | `Empty_communal_kitchen_dry_trash`; `Empty_communal_kitchen_wet_trash` |
| 7 | Inspect or replace kitchen propane | `Inspect_kitchen_propane_supply`; trained-only `Replace_kitchen_propane_cylinder` |
| 8 | Kitchenware clean | `Wash_communal_kitchenware` |
| 10–14 | Buffer Bush function, inflation, cleanup, access, and mechanics | `Prepare_Buffer_Bush` |
| 15 | Clear common area | `Clear_common_area` |
| 16 | Rake public dance floor | `Rake_public_dance_floor` |
| 17 | Public-area belongings to lost and found | `Clear_public_area_belongings` |
| 18–19 | EMT mechanics and puddles | `Inspect_EMT_shade` |
| 21–23, 26 | Trash bins, bags, and dumpster | `Service_communal_trash_bins` |
| 24–25 | Campwide MOOP and belongings | `Sweep_camp_for_MOOP`; area-clearing tasks |
| 27–29 | Empty, crush, and deliver aluminum cans | `Recycle_aluminum_cans` uses current 2026 Recycle Camp details |
| 32–33 | Flame structure and vaporizer-hose valve state | `Inspect_flame_effect_system` |
| 34–39 | Shower pump, puddles, cleaning, hair, and standing water | `Inspect_and_clean_shower` |
| 40–42 | Toilet service, paper, and full tank | `Inspect_camp_porta_potties`; `Coordinate_camp_service_visit` |
| 43 | Gray-water IBC leak and level | `Inspect_gray-water_IBC` |
| 44 | Fresh-water level | `Read_fresh_water_tank_level` |
| 45 | Clean bar top | `Clean_bar` |
| 46–47 | Common yurt and surrounding MOOP | `Clear_common_yurt_and_yurt_area` |
| 48–49 | Generator reading and escalation | `Read_generator_fuel_level` |
| 50 | Five-bag morning ice run | `Get_camp_ice` |
| 51 | Charge radios and impact-driver batteries | `Charge_camp_radios`; `Charge_impact_driver_batteries` |

## Infra Lead checklist

| Rows | Source instruction | Canonical coverage |
| --- | --- | --- |
| 2 | Find servicing vouchers | Runtime; approved method comes from the Dominatrix |
| 3–5 | Obtain toilet, gray-water, and RV service | `Coordinate_camp_service_visit` |
| 6 | “Continue this checklist” placeholder | Excluded; it contains no outcome |

## Shower and toilet instructions

`Use_camp_shower` covers the Shower sheet: a three-minute maximum, water off
while soaping, personal items contained, hair and trash removed, surfaces
rinsed, pump run after use, and leaks or pump failures escalated. Humor and the
ambiguous shared-shower exception are not operational requirements.

`Inspect_camp_porta_potties` and the porta-potty item cover the Toilet sheet:
only human waste and one-ply paper enter the tank; lids and doors close; spills
are cleaned without putting wipes in the tank; full or contaminated toilets are
closed and escalated. Odor folklore and campaign jokes are excluded.

## Liaison shift

Rows 2–18 and 20–30 map to `Host_scheduled_artist`: review the rider, locate
the artist 30 minutes early, introduce the sound team, provide water, route the
pairing gift through `Serve_wine` and `Serve_cheese_pairing`, record actual set
times, remain available, prepare the next artist, thank the artist, and handle a
missing artist through the Music Lead and Dominatrix. Named-person escalation
and private contact methods are replaced by stable roles. The unspecified
“nicer bottle” is excluded until the Bar Lead approves a product and legal
handoff method.

## Pre-event checklist

| Rows | Source instruction | Canonical coverage |
| --- | --- | --- |
| 2–4 | Stage gear, stage state, and recorder | `Prepare_event_stage` |
| 5 | Dance-floor MOOP | `Rake_public_dance_floor` |
| 9–10 | Bar ready and ice available | `Prepare_bar_for_service`; `Get_camp_ice` |
| 11, 22 | Two drinking-water dispensers full | `Fill_kitchen_drinking_water_dispensers` |
| 14–19 | Buffer Bush readiness | `Prepare_Buffer_Bush` |
| 21 | Replace kitchen propane | `Replace_kitchen_propane_cylinder` |
| 23 | Refuel generators | `Coordinate_generator_refueling` |
| 24 | Public-shade integrity | `Inspect_EMT_shade` |
| 26–27 | Generator gauge and escalation | `Read_generator_fuel_level`; conflicting threshold remains owned by Fuel Lead |

## Bar shift

| Rows | Source instruction | Canonical coverage |
| --- | --- | --- |
| 2 | Clean bar when needed | `Clean_bar`; `Prepare_bar_for_service` |
| 3–6 | Cooler, wine, ice quantities, trash bins, and pairing briefing | `Prepare_bar_for_service` |
| 7–9 | Do not hand out cans, half-can serving, age verification | `Serve_wine` |
| 10 | Assport interaction | `Provide_Assport_experience` adds current consent requirements |
| 11 | Enjoy and talk with people | Excluded as tone, not a completion criterion |

The source sends cans to trash. Current 2026 guidance instead controls:
`Serve_wine` crushes empties into aluminum collection and
`Recycle_aluminum_cans` takes eligible cans to Recycle Camp.

## Afternoon checklist

Rows 2 and 34–35 map to `Read_generator_fuel_level`. Rows 5–12 map to the
same kitchen, trash, propane, refrigerator, dishwashing, and drinking-water
tasks used by Morning and Pre-event. Rows 14–18 map to `Prepare_Buffer_Bush`;
20–21 to `Clear_common_area`; 23–24 to `Inspect_EMT_shade`; and 26–31 to
`Recycle_aluminum_cans`, `Service_communal_trash_bins`, and
`Sweep_camp_for_MOOP`.

Row 32 says to erase completed checkmarks. It is replaced by durable runtime
status, initials, and completion time; completed execution evidence is not
erased.

## Cheese shift

| Rows | Source phase | Canonical coverage |
| --- | --- | --- |
| 2–8 | Health, handwashing, PPE, surface sanitation, cheese temperature, labeling, cold trays, and permit checklist | `Prepare_cheese_station` |
| 10–13 | Protected small-batch cheese and cracker service through 6:00–8:30 p.m. | `Serve_cheese_pairing` |
| 15–18 | Disposition of leftovers, three-basin wash/rinse/sanitize, air drying, and storage | `Close_cheese_station` |

The canonical tasks add the current 41°F cold-holding limit, sanitizer
concentration and contact time, handwashing order, food protection, temperature
records, and a rule against saving exposed food with unknown history.

## Post-event checklist

| Rows | Source instruction | Canonical coverage |
| --- | --- | --- |
| 2 | Help sound engineers pack the stage | `Pack_DJ_gear_after_event`; `Strike_sound_system` for full Strike |
| 3, 8 | Clean stage | `Clean_event_stage` |
| 4 | Turn off flame-effect valves | Licensed-only `Shut_down_flame_effects`; `Shut_down_Zimmer_vaporizer`; `Complete_flame_effect_postcheck` |
| 5 | Charge impact drivers | `Charge_impact_driver_batteries` |
| 6 | Clean bar | `Clean_bar` |
| 7 | Buffer Bush lit, inflated, operational | `Prepare_Buffer_Bush` |
| 9–10 | Close truck and container | `Secure_equipment_truck_and_container` |
| 11 | Read generator gauge | `Read_generator_fuel_level` |

## Flame Effect checklist

| Source phase | Canonical coverage |
| --- | --- |
| Pre-operation checks | `Inspect_flame_effect_system` |
| Zimmer startup | `Start_Zimmer_vaporizer` |
| Effect startup | `Start_flame_effects` |
| Active attendance and wind response | `Operate_flame_effects` |
| Effect shutdown | `Shut_down_flame_effects` |
| Zimmer shutdown | `Shut_down_Zimmer_vaporizer` |
| Post-operation | `Complete_flame_effect_postcheck` |

The workbook's unknown valve names, voltage and temperature ranges, and
ambiguous “decide on” power instruction are not guessed. They must be defined
in the current `Flame_Effect_Operating_Procedure` for the actual installation.
Only a trained operator physically holding the effect's FAST license may
operate it.

## Strike plan

The source tab declares itself **OUT OF DATE**. Its physical asset groups are
retained as evidence and rewritten into current work packages; old leaders,
team assignments, personal tents, and crude team names are excluded.

| Source asset or activity | Canonical coverage |
| --- | --- |
| Bar and remaining alcohol | `Strike_bar` |
| Kitchen, utensils, tables, coolers, and carport | `Strike_communal_kitchen` |
| Benches, swings, chairs, rugs, and cushions | `Strike_camp_furniture` |
| Sound gear and stage scaffold | `Strike_sound_system`; `Strike_event_stage` |
| Camp sign | `Strike_camp_sign` |
| Common yurt | `Strike_common_yurt` |
| Buffer Bush | `Strike_Buffer_Bush` |
| Tower and propane | `Strike_fuel_and_propane_area`; `Strike_camp_tower` |
| Arch and red carpet | `Strike_camp_arch` |
| Shower and sink | `Strike_camp_shower_and_sink` |
| EMT shade, tarps, straps, poles, anchors, and hardware | `Strike_EMT_shade` |
| Camp lighting | `Strike_camp_lighting` |
| Fence | `Strike_camp_fence` |
| Trash | `Service_communal_trash_bins` |
| Truck runners, loading, inventory, and securement | `Load_strike_truck` |
| Final MOOP patrol | `Sweep_camp_for_MOOP` |

The old shade sequence removed anchors before sail-producing coverings. The
canonical task keeps the structure anchored until side and roof coverings are
controlled and removed.

## Build list 2025

The tab is principally a prior-year calendar. Repeated calendar envelopes,
dates, travel, personal assignments, and duration estimates are not canonical
procedures. Physical work titles map as follows.

| Source title | Canonical coverage |
| --- | --- |
| Prep boxes and load truck | `Prepare_build_truck` |
| Assemble stages / scaffold | `Build_event_stage` |
| Build Kitchen | `Set_up_communal_kitchen` |
| EMT Build / More EMT Build / Main Shade Setup | `Assemble_EMT_shade` |
| Sink Build / Shower Build / Shower and Sink | `Set_up_camp_shower_and_sink` |
| Sound setup / antenna | `Set_up_sound_system` |
| Buffer Bush Assembly | `Assemble_Buffer_Bush` |
| Bar Setup | `Set_up_bar` |
| Night Lights Setup / Lights Setup | `Install_camp_lighting` |
| Fix common Yurt | `Set_up_common_yurt` |
| Attach Fence | `Install_camp_fence` |
| 1/2-inch poofer assembly | `Install_flame_effect_system` |
| Common furniture | `Set_up_camp_furniture` |
| Camp sign, arch, and tower evidenced by Strike | `Install_camp_sign`; `Assemble_camp_arch`; `Assemble_camp_tower` |
| Generator or water delivery | `Coordinate_generator_refueling`; `Coordinate_camp_service_visit` |
| FAST inspection | `Install_flame_effect_system` |
| Strike EMT, tower, propane, benches, stage, kitchen | Corresponding `Strike_*` tasks |
| Unload | `Unload_strike_truck` |
| Cleanup | `Service_communal_trash_bins`; `Sweep_camp_for_MOOP` |

These prior-year planning entries are excluded from procedure XML: calendar
container records, travel and lodging, vehicle rental, vendor delivery details,
payment-account activation, voucher collection, procurement, personal names,
private contact text, and general parent events such as “Build on Playa” or
“Burn Week.” Food-permit presence is verified by `Prepare_cheese_station`; the
application itself remains a current-year Food Lead administrative action.

| Excluded source title group | Reason |
| --- | --- |
| Build in Nevada City; Build on Playa; Build Weekend at Ranch; Burn Week; Strike | Calendar envelopes, not individual outcomes |
| Drive to Playa or off-playa destinations; Stay in Reno | Personal travel and lodging |
| Get Enterprise truck; Drop Truck | Rental logistics |
| Meet Placers; Container Delivery | Current-year runtime placement and provider coordination |
| Activate Petrol Account; Get United vouchers; Get food permit | Administrative work containing current account, payment, permit, or contact data |
| Get New Scaffold | Procurement, not use of the acquired scaffold |
| Print checklists | Document production; generated outputs are built from XML rather than represented as a camp task |
| Go to HEAT | Too ambiguous to identify an outcome or responsible system |

“Heat Trenches” is excluded because the source does not define the object or
method and current Burning Man guidance strongly discourages buried electrical
cables. The Power Lead must clarify the intended outcome before a task can be
added.

## Excluded workbook tabs

| Tab | Reason |
| --- | --- |
| Dominatrix List | Personal schedule; runtime roster |
| Camp Layout 2024 | Prior-year layout with personal sleeping and vehicle data |
| strike teams | Outdated personal assignments |
| Sheet50 | Protected ticket, phone, and member data |
| WhatsAppExport_20240620 | Protected contact export |
| WhatsappExtract 08-02 | Protected contact export |
| Communication | Marked deprecated and unrelated to task execution |

## Required field validation

The inventory and logical procedures are complete to the available source, but
these facts cannot be responsibly invented:

1. The Build Lead must populate `Build_Book` with actual drawings, part counts,
   anchor locations, crew counts, lift/lowering sequences, load limits, and
   final-state photographs before any Build or Strike work package is used.
2. The Flame Lead must populate the actual valve and control IDs, voltage,
   thermocouple ranges, pressure, reflow time, and emergency shutdown sequence;
   FAST must approve the installed effect and issue its physical license.
3. The Propane Lead must replace the provisional kitchen-cylinder description
   with the actual cylinder size, connection, regulator, and matching appliance
   manual.
4. The Fuel Lead must resolve the generator threshold conflict and confirm the
   actual generator fuel type and service method.
5. The Water Lead must define the low-water trigger and current approved
   fresh-water and gray-water service methods.
6. The Food Lead must confirm the 2026 permit, actual products, sanitizer label,
   and service plan before public cheese service.
7. On-playa maps, rosters, assignments, provider methods, and payment
   authorization must be supplied at runtime without committing protected data.

Until the relevant lead supplies and validates these details, the affected task
card is a controlled work-package boundary, not permission to improvise.
