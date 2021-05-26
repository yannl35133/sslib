from .logic import Logic
from paths import RANDO_ROOT_PATH
import yaml
from collections import OrderedDict, defaultdict
from dataclasses import dataclass
from .constants import POTENTIALLY_REQUIRED_DUNGEONS
from util import textbox_utils

ALWAYS_REQUIRED_LOCATIONS = [
    'Thunderhead - Levias',
    "Sky - Kina's Crystals",
    "Skyloft - Peater/Peatrice's Crystals",
    'Batreaux - 80 Crystals',
]

SOMETIMES_LOCATIONS = [
    "Lanayru Sand Sea - Roller Coaster Minigame",
    'Skyloft Academy - Pumpkin Archery - 600 Points',
    'Sky - Lumpy Pumpkin Harp Minigame',
    "Sky - Fun Fun Island Minigame",
    'Thunderhead - Bug Island minigame',
    'Batreaux - 70 Crystals Second Reward',
    'Batreaux - 70 Crystals',
    'Batreaux - 50 Crystals',
    "Skyloft Academy - Owlan's Crystals",
    "Skyloft Village - Sparrot's Crystals",
    "Lanayru - On Top of Lanayru Mining Facility",
    "Skyloft - Waterfall Goddess Chest", # stronghold cube
    "Sky - Beedle's Island Goddess Chest", # goddess cube in ToT area
]

HINTABLE_ITEMS = \
    ["Clawshots"] + \
    ["Progressive Beetle"] * 2 + \
    ["Progressive Sword"] * 4 + \
    ["Emerald Tablet"] * 1 + \
    ["Ruby Tablet"] * 1 + \
    ["Amber Tablet"] * 1 + \
    ["Goddess Harp"] * 1 + \
    ["Water Scale"] * 1 + \
    ["Fireshield Earrings"] * 1


class GossipStoneHint:
    def to_gossip_stone_text(self) -> str:
        raise NotImplementedError("abstract")

    def to_spoiler_log_text(self) -> str:
        raise NotImplementedError("abstract")

@dataclass
class GossipStoneHintWrapper(GossipStoneHint):
    primary_hint: GossipStoneHint
    secondary_hint: GossipStoneHint

    def to_gossip_stone_text(self) -> str:
        return ''

    def to_spoiler_log_text(self) -> str:
        return f"{self.primary_hint.to_spoiler_log_text()} / {self.secondary_hint.to_spoiler_log_text()}"

@dataclass
class LocationGossipStoneHint(GossipStoneHint):
    location_name: str
    item: str

    def to_gossip_stone_text(self) -> str:
        zone, specific_loc = Logic.split_location_name_by_zone(self.location_name)
        return textbox_utils.break_lines(
            f"<r<{zone} - {specific_loc}>> has <y<{self.item}>>"
        )

    def to_spoiler_log_text(self) -> str:
        return f"{self.location_name} has {self.item}"


@dataclass
class ItemGossipStoneHint(GossipStoneHint):
    location_name: str
    item: str

    def to_gossip_stone_text(self) -> str:
        zone, specific_loc = Logic.split_location_name_by_zone(self.location_name)
        return textbox_utils.break_lines(
            f"<y<{self.item}>> can be found at <r<{zone}: {specific_loc}>>"
        )

    def to_spoiler_log_text(self) -> str:
        return f"{self.item} is on {self.location_name}"


@dataclass
class WayOfTheHeroGossipStoneHint(GossipStoneHint):
    zone: str

    def to_gossip_stone_text(self) -> str:
        return textbox_utils.break_lines(
            f"The <b+<Spirit of the Sword>> guides the goddess' chosen hero to <r<{self.zone}>>"
        )

    def to_spoiler_log_text(self) -> str:
        return f"{self.zone} is WotH"


@dataclass
class BarrenGossipStoneHint(GossipStoneHint):
    zone: str

    def to_gossip_stone_text(self) -> str:
        return textbox_utils.break_lines(
            f"They say that those who travel to <r<{self.zone}>> will never find anything for their quest"
        )

    def to_spoiler_log_text(self) -> str:
        return f"{self.zone} is barren"


@dataclass
class EmptyGossipStoneHint(GossipStoneHint):
    text: str

    def to_gossip_stone_text(self) -> str:
        return self.text

    def to_spoiler_log_text(self) -> str:
        return self.text


class Hints:
    def __init__(self, logic: Logic):
        with (RANDO_ROOT_PATH / "hints.yaml").open() as f:
            self.stonehint_definitions: dict = yaml.safe_load(f)
        self.logic = logic
        for hintname, hintdef in self.stonehint_definitions.items():
            if self.logic.rando.options['logic-mode'] == 'No Logic':
                hintdef["Need"] = Logic.parse_logic_expression(hintname, "Nothing")
            else:
                hintdef["Need"] = self.logic.macros[hintname]
        self.hints = OrderedDict()

    def do_junk_hints(self):
        for hintname in self.stonehint_definitions.keys():
            self.hints[hintname] = EmptyGossipStoneHint(text='Useless hint')

    def do_normal_hints(self):
        location_hints = []
        item_hints = []
        total_stonehints = len(self.stonehint_definitions)
        needed_always_hints = self.logic.filter_locations_for_progression(ALWAYS_REQUIRED_LOCATIONS)
        # in shopsanity, we need to hint some beetle shop items
        # add them manually, cause they need to be kinda weirdly implemented because of bug net
        if self.logic.rando.options['shop-mode'] == 'Randomized' and \
                'expensive' not in self.logic.rando.options['banned-types']:
            needed_always_hints.append('Beedle - 1200 Rupee Item')
            needed_always_hints.append('Beedle - 1600 Rupee Item')
        if self.logic.rando.options['song-hints'] == 'None':
            needed_always_hints.append('Skyloft Silent Realm - Stone of Trials')
            needed_always_hints.append('Faron Silent Realm - Water Scale')
            needed_always_hints.append('Lanayru Silent Realm - Clawshots')
            needed_always_hints.append('Eldin Silent Realm - Fireshield Earrings')
        needed_sometimes_hints = self.logic.filter_locations_for_progression(SOMETIMES_LOCATIONS)

        hints_left = total_stonehints
        hinted_locations = []
        # create woth hints
        woth_hints_count = self.logic.rando.options['woth-hints']
        woth_hints = []
        if woth_hints_count > 0:  # avoid doing the additional woth calculations if it isn't necessary
            woth_locations = {}
            for wothloc, item in self.logic.rando.woth_locations.items():
                if self.logic.rando.options['small-key-mode'] not in ['Anywhere', 'Lanayru Caves Key Only']:
                    # don't hint small keys unless keysanity is on
                    if item.endswith('Small Key'):
                        continue
                elif self.logic.rando.options['small-key-mode'] == 'Lanayru Caves Key Only':
                    if item.endswith('Small Key') and item != 'LanayruCaves Small Key':
                        continue

                if self.logic.rando.options['boss-key-mode'] not in ['Anywhere']:
                    # don't hint boss keys unless keysanity is on
                    if item.endswith('Boss Key'):
                        continue

                zone, specific_loc = Logic.split_location_name_by_zone(wothloc)
                if zone not in woth_locations.keys():  # we only need each zone to appear once
                    woth_locations[zone] = [wothloc]
                else:
                    woth_locations[zone].append(wothloc)
            woth_zones = []
            for zone, locations in woth_locations.items():
                woth_zones.append(zone)
            if len(woth_zones) < woth_hints_count:  # there are not enough woth zones to fill the number of hints
                woth_hints_count = len(woth_locations)  # so to prevent odd behavior we cap it at the number of zones
                # this also means that the missing hint slots will be filled by random hints
            self.logic.rando.rng.shuffle(woth_zones)
            for i in range(woth_hints_count):
                loc = self.logic.rando.rng.choice(woth_locations[woth_zones[i]])
                if loc not in hinted_locations:
                    woth_hints.append(loc)
                    hinted_locations.append(loc)
                    hints_left -= 1

        # create barren hints
        barren_hints_count = self.logic.rando.options['barren-hints']
        barren_hints = []
        if barren_hints_count > 0:
            region_barren = self.logic.get_barren_regions().copy()
            barren_zones = []
            for zone in region_barren.keys():
                if 'Silent Realm' in zone:
                    continue  # don't hint barren silent realms since they are an always hint
                if self.logic.rando.options['empty-unrequired-dungeons']:
                    # avoid placing barren hints for unrequired dungeons in race mode
                    if self.logic.rando.options['skip-skykeep'] and zone == 'Skykeep':
                        # skykeep is always barren when race mode is on a dn skykeep is skipped
                        continue
                    if zone in POTENTIALLY_REQUIRED_DUNGEONS and zone not in self.logic.rando.required_dungeons:
                        # unrequired dungeons are always barren in race mode
                        continue
                if zone == 'Skykeep':
                    # exclude skykeep from the eligible barren locations if it has no open checks
                    if self.logic.rando.options['map-mode'] not in ['Removed, Anywhere'] or self.logic.rando.options['small-key-mode'] not in ['Anywhere']:
                        continue
                if region_barren[zone]:
                    barren_zones.append(zone)
            self.logic.rando.rng.shuffle(barren_zones)
            if len(barren_zones) < barren_hints_count:
                barren_hints_count = len(barren_zones)
            for i in range(barren_hints_count):
                barren_hints.append(barren_zones.pop())
                hints_left -= 1

        # create location hints
        location_hints_left = self.logic.rando.options['location-hints']
        for location in needed_always_hints:
            if location_hints_left <= 0:
                break
            if location not in hinted_locations:
                location_hints.append(location)
                hinted_locations.append(location)
                hints_left -= 1
                location_hints_left -= 1
        while location_hints_left > 0:
            for location in self.logic.rando.rng.sample(needed_sometimes_hints,
                                                        k=min(hints_left, len(needed_sometimes_hints))):
                if location not in hinted_locations:
                    location_hints.append(location)
                    hinted_locations.append(location)
                    hints_left -= 1
                    location_hints_left -= 1

        # create  the item hints
        hintable_items = HINTABLE_ITEMS.copy()
        self.logic.rando.rng.shuffle(hintable_items)
        for i in range(self.logic.rando.options['item-hints']):
            hinted_item = hintable_items.pop()
            for location, item in self.logic.done_item_locations.items():
                if item == hinted_item and location not in item_hints and location not in hinted_locations:
                    item_hints.append(location)
                    hinted_locations.append(location)
                    hints_left -= 1
                    break

        all_locations_without_hint = self.logic.filter_locations_for_progression((loc for loc in self.logic.done_item_locations if not loc in location_hints and not loc in self.logic.prerandomization_item_locations))
        while hints_left > 0 and all_locations_without_hint:
            # add completely random locations if there are otherwise empty stones
            location_to_hint = self.logic.rando.rng.choice(all_locations_without_hint)
            all_locations_without_hint.remove(location_to_hint)
            location_hints.append(location_to_hint)
            hints_left -= 1
        self._place_hints_for_locations(location_hints, item_hints, woth_hints, barren_hints)

    def do_bingo_hints(self):
        important_items = {"Progressive Sword", "Goddess Harp", "Clawshots", "Water Scale", "Fireshield Earrings"}
        if self.logic.rando.options['shop-mode'] == 'Randomized':
            important_items.add("Bug Net")
        hint_locations = []
        for location, item in self.logic.done_item_locations.items():
            if item in important_items:
                hint_locations.append(location)
        assert len(hint_locations) <= len(self.stonehint_definitions), f"need {len(hint_locations)} locations, but only {len(self.stonehint_definitions)} stones available"

        all_locations_without_hint = self.logic.filter_locations_for_progression((loc for loc in self.logic.done_item_locations if not loc in hint_locations and not loc in self.logic.prerandomization_item_locations))
        while len(hint_locations) < len(self.stonehint_definitions) and all_locations_without_hint:
            # add completely random locations if there are otherwise empty stones
            location_to_hint = self.logic.rando.rng.choice(all_locations_without_hint)
            all_locations_without_hint.remove(location_to_hint)
            hint_locations.append(location_to_hint)

        self._place_hints_for_locations(hint_locations, [], [], [])

    def _place_hints_for_locations(self, location_hints, item_hints, woth_hints, barren_hints):
        hint_locations = location_hints + item_hints + woth_hints
        # make sure hint locations aren't locked by the item they hint
        hint_banned_stones = defaultdict(set)
        for hint_location in hint_locations:
            hinted_item = self.logic.done_item_locations[hint_location]
            if hinted_item in self.logic.all_progress_items:
                for gossipstone_name, gossipstone_def in self.stonehint_definitions.items():
                    if not self.logic.can_reach_restricted([hint_location], gossipstone_def["Need"]):
                        hint_banned_stones[gossipstone_name].add(hint_location)
        stones_to_banned_locs_sorted = sorted(hint_banned_stones.items(), key=lambda x: len(x[1]), reverse=True)

        if len(hint_locations) < len(self.stonehint_definitions):
            hint_locations.extend([None]*(len(self.stonehint_definitions) - len(hint_locations)))
        unhinted_locations = hint_locations.copy()

        hint_to_location = {}
        # place locations that are restricted in locations
        for gossipstone_name, banned_locations in stones_to_banned_locs_sorted:
            valid_locations = [loc for loc in unhinted_locations if not loc in banned_locations]
            if len(valid_locations) == 0:
                print(f"no valid location for {gossipstone_name} in seed {self.logic.rando.seed}")
                loc_to_hint = unhinted_locations[0]
                # raise Exception('no valid location to place hint!')
            else:
                loc_to_hint = self.logic.rando.rng.choice(valid_locations)
            hint_to_location[gossipstone_name] = loc_to_hint
            unhinted_locations.remove(loc_to_hint)
        # place locations that aren't restricted and also fill rest of locations
        for gossipstone_name in [name for name in self.stonehint_definitions if not name in hint_to_location]:
            if len(unhinted_locations) == 0:
                # placeholder
                hint_to_location[gossipstone_name] = None
                continue
            loc_to_hint = self.logic.rando.rng.choice(unhinted_locations)
            unhinted_locations.remove(loc_to_hint)
            hint_to_location[gossipstone_name] = loc_to_hint
        anywhere_hints = barren_hints + []
        self.logic.rando.rng.shuffle(anywhere_hints)
        for gossipstone_name in self.stonehint_definitions:
            loc_to_hint = hint_to_location[gossipstone_name]
            if loc_to_hint is None:
                # place barren and woth hints at locations with no hints
                hint = anywhere_hints.pop()
                if hint in woth_hints:
                    self.hints[gossipstone_name] = WayOfTheHeroGossipStoneHint(zone=hint)
                elif hint in barren_hints:
                    self.hints[gossipstone_name] = BarrenGossipStoneHint(zone=hint)
                else:
                    self.hints[gossipstone_name] = EmptyGossipStoneHint(text='--PLACEHOLDER--')
            else:
                if loc_to_hint in location_hints:
                    self.hints[gossipstone_name] = LocationGossipStoneHint(
                            location_name=loc_to_hint,
                            item=self.logic.done_item_locations[loc_to_hint]
                    )
                elif loc_to_hint in item_hints:
                    self.hints[gossipstone_name] = ItemGossipStoneHint(
                        location_name=loc_to_hint,
                        item=self.logic.done_item_locations[loc_to_hint]
                    )
                elif loc_to_hint in woth_hints:
                    zone, specific_loc = Logic.split_location_name_by_zone(loc_to_hint)
                    self.hints[gossipstone_name] = WayOfTheHeroGossipStoneHint(
                        zone=zone
                    )
                else:
                    raise Exception(f"Unable to identify hint type for location {loc_to_hint}")
