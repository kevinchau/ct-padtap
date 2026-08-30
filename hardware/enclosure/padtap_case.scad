// PadTap under-panel sled
// Tesla Cybertruck center-console cavity — VHB the lid to the underside of a panel.
// Units: millimetres. Print PETG, 0.2 mm layers, 4 perimeters, 30% gyroid.
//
//   openscad -o padtap_base.stl -D PART=\"base\" padtap_case.scad
//   openscad -o padtap_lid.stl  -D PART=\"lid\"  padtap_case.scad

PART = "base"; // "base" | "lid" | "preview"

outer_l = 108;
outer_w = 56;
base_h  = 16.2;
lid_t   = 1.8;
lip_h   = 1.4;
wall    = 1.6;
floor_t = 1.6;
corner  = 3.0;

// Interior after walls
inner_l = outer_l - 2 * wall;
inner_w = outer_w - 2 * wall;
inner_h = base_h - floor_t;

// Cable comb (west) — U-slots, drop wires in from above, lid clamps
comb_w    = 4.4;
comb_gap  = 8.0;
comb_saddle = 4.2; // remaining wall under the slot
comb_count = 3;

// Barrel jack (east) — 5.5 mm panel jack, 8.2 mm hole
barrel_d = 8.2;
barrel_z = 6.5; // center from floor top (inside)

// USB-C window (south) — SuperMini, tape over after flash
usb_w = 9.6;
usb_h = 3.8;
usb_x = 72; // from outer origin
usb_z = 4.2;

// LED membranes in lid (0.4 mm floor so light shows)
led_d = 3.2;
led1_x = 74;
led2_x = 82;
led_y  = 40;

// Vents on long walls
vent_w = 10;
vent_h = 2.2;
vent_z = 6;

// M2.5 corners
boss_d = 6.2;
screw_d = 2.7;
insert_d = 3.6;
insert_h = 4.2;
boss_inset = 5.5;

// VHB pockets on lid exterior (mount face)
vhb = 12;

$fn = 48;

module round_rect(l, w, h, r) {
  hull() {
    for (x = [r, l - r])
      for (y = [r, w - r])
        translate([x, y, 0]) cylinder(h = h, r = r);
  }
}

module shell_body(h) {
  difference() {
    round_rect(outer_l, outer_w, h, corner);
    translate([wall, wall, -0.1])
      round_rect(inner_l, inner_w, h + 0.2, max(0.4, corner - wall));
  }
}

module cable_comb() {
  cx0 = wall + 10;
  for (i = [0 : comb_count - 1]) {
    translate([-0.2, cx0 + i * comb_gap, floor_t + comb_saddle])
      cube([wall + 0.4, comb_w, inner_h + 1]);
  }
}

module barrel_hole() {
  translate([outer_l + 0.1, outer_w / 2, floor_t + barrel_z])
    rotate([0, -90, 0])
      cylinder(h = wall + 0.4, d = barrel_d);
}

module usb_slot() {
  translate([usb_x, -0.2, floor_t + usb_z])
    cube([usb_w, wall + 0.4, usb_h]);
}

module vents() {
  for (y = [-0.2, outer_w - wall - 0.2]) {
    for (x = [18, 40, 62]) {
      translate([x, y, floor_t + vent_z])
        cube([vent_w, wall + 0.4, vent_h]);
    }
  }
}

module bosses(h, hole_d, hole_h, z0) {
  for (x = [boss_inset, outer_l - boss_inset])
    for (y = [boss_inset, outer_w - boss_inset])
      translate([x, y, z0]) {
        difference() {
          cylinder(h = h, d = boss_d);
          translate([0, 0, -0.1])
            cylinder(h = hole_h + 0.2, d = hole_d);
        }
      }
}

module padtap_base() {
  difference() {
    union() {
      // floor
      round_rect(outer_l, outer_w, floor_t, corner);
      // walls
      shell_body(base_h);
      // lip shelf for lid (inner ledge)
      translate([wall / 2, wall / 2, base_h - lip_h])
        difference() {
          round_rect(outer_l - wall, outer_w - wall, lip_h, corner - wall / 2);
          translate([wall / 2, wall / 2, -0.1])
            round_rect(inner_l, inner_w, lip_h + 0.2, max(0.2, corner - wall));
        }
      bosses(inner_h - 0.4, insert_d, insert_h, floor_t);
    }
    cable_comb();
    barrel_hole();
    usb_slot();
    vents();
    // through-holes in floor unused — inserts from inside
  }
}

module padtap_lid() {
  difference() {
    union() {
      round_rect(outer_l, outer_w, lid_t, corner);
      // lip that nests into the base
      translate([wall / 2 + 0.15, wall / 2 + 0.15, lid_t])
        round_rect(outer_l - wall - 0.3, outer_w - wall - 0.3, lip_h - 0.15, corner - wall / 2);
    }
    // screw through
    for (x = [boss_inset, outer_l - boss_inset])
      for (y = [boss_inset, outer_w - boss_inset])
        translate([x, y, -0.1])
          cylinder(h = lid_t + lip_h + 0.3, d = screw_d);
    // countersink
    for (x = [boss_inset, outer_l - boss_inset])
      for (y = [boss_inset, outer_w - boss_inset])
        translate([x, y, -0.01])
          cylinder(h = 1.0, d1 = 5.0, d2 = screw_d);
    // LED membranes: through-cut to 0.4 mm remaining
    for (x = [led1_x, led2_x])
      translate([x, led_y, 0.4])
        cylinder(h = lid_t + lip_h, d = led_d);
    // comb clamp ribs are extra — cut matching slots so wires aren't pinched to zero
    cx0 = wall + 10;
    for (i = [0 : comb_count - 1])
      translate([-0.2, cx0 + i * comb_gap + 0.3, lid_t + 0.4])
        cube([wall + 2, comb_w - 0.6, lip_h]);
    // VHB pockets on the MOUNT FACE (z=0, printed against bed = glossy)
    for (x = [12, outer_l - 12 - vhb])
      for (y = [8, outer_w - 8 - vhb])
        translate([x, y, -0.01])
          cube([vhb, vhb, 0.35]);
  }
}

if (PART == "base") padtap_base();
else if (PART == "lid") padtap_lid();
else {
  padtap_base();
  translate([0, 0, base_h + 8]) padtap_lid();
}
