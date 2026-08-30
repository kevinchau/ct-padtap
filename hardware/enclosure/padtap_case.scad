// PadTap under-panel sled — sized to Rev A.1 (58 × 34 mm PCB)
// Units: millimetres. Print PETG, 0.2 mm layers, 4 perimeters, 30% gyroid.
//
//   openscad -o padtap_base.stl -D PART=\"base\" padtap_case.scad
//   openscad -o padtap_lid.stl  -D PART=\"lid\"  padtap_case.scad

PART = "base"; // "base" | "lid" | "preview"

outer_l = 64;
outer_w = 40;
base_h  = 13.6;
lid_t   = 1.6;
lip_h   = 1.2;
wall    = 1.5;
floor_t = 1.5;
corner  = 2.5;

inner_l = outer_l - 2 * wall;
inner_w = outer_w - 2 * wall;
inner_h = base_h - floor_t;

// PCB origin in this shell (wall + clearance)
board_ox = 2.0;
board_oy = 3.0;

// Cable comb (west) — lines up with J1 VIN / GND / LIN
comb_w      = 4.0;
comb_gap    = 6.0;
comb_saddle = 3.6;
comb_count  = 3;
comb_y0     = 11.0;

// Barrel (east) — PCB J2 at board (55.4, 22.5)
barrel_d = 8.2;
barrel_z = 6.0;
barrel_y = board_oy + 22.5;

// USB-C (south) — connector centre at board x = 30
usb_w = 9.6;
usb_h = 3.6;
usb_x = board_ox + 30 - usb_w / 2;
usb_z = 2.2;

// LED membranes over 0805s at board (51.35, 16.8) and (51.35, 14.4)
led_d  = 2.8;
led1_x = board_ox + 51.35;
led1_y = board_oy + 16.8;
led2_x = board_ox + 51.35;
led2_y = board_oy + 14.4;

// Vents
vent_w = 8;
vent_h = 2.0;
vent_z = 5.2;

// M2.5 at PCB holes (3,3) (55,3) (3,31) (55,31)
boss_d   = 5.5;
screw_d  = 2.7;
insert_d = 3.4;
insert_h = 3.8;
bosses   = [[board_ox + 3, board_oy + 3],
            [board_ox + 55, board_oy + 3],
            [board_ox + 3, board_oy + 31],
            [board_ox + 55, board_oy + 31]];

vhb = 10;

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
  for (i = [0 : comb_count - 1]) {
    translate([-0.2, comb_y0 + i * comb_gap, floor_t + comb_saddle])
      cube([wall + 0.4, comb_w, inner_h + 1]);
  }
}

module barrel_hole() {
  translate([outer_l + 0.1, barrel_y, floor_t + barrel_z])
    rotate([0, -90, 0])
      cylinder(h = wall + 0.4, d = barrel_d);
}

module usb_slot() {
  translate([usb_x, -0.2, floor_t + usb_z])
    cube([usb_w, wall + 0.4, usb_h]);
}

module vents() {
  for (y = [-0.2, outer_w - wall - 0.2]) {
    for (x = [14, 38]) {
      translate([x, y, floor_t + vent_z])
        cube([vent_w, wall + 0.4, vent_h]);
    }
  }
}

module boss_set(h, hole_d, hole_h, z0) {
  for (p = bosses)
    translate([p[0], p[1], z0]) {
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
      round_rect(outer_l, outer_w, floor_t, corner);
      shell_body(base_h);
      translate([wall / 2, wall / 2, base_h - lip_h])
        difference() {
          round_rect(outer_l - wall, outer_w - wall, lip_h, corner - wall / 2);
          translate([wall / 2, wall / 2, -0.1])
            round_rect(inner_l, inner_w, lip_h + 0.2, max(0.2, corner - wall));
        }
      boss_set(inner_h - 0.4, insert_d, insert_h, floor_t);
    }
    cable_comb();
    barrel_hole();
    usb_slot();
    vents();
  }
}

module padtap_lid() {
  difference() {
    union() {
      round_rect(outer_l, outer_w, lid_t, corner);
      translate([wall / 2 + 0.15, wall / 2 + 0.15, lid_t])
        round_rect(outer_l - wall - 0.3, outer_w - wall - 0.3, lip_h - 0.15, corner - wall / 2);
    }
    for (p = bosses)
      translate([p[0], p[1], -0.1])
        cylinder(h = lid_t + lip_h + 0.3, d = screw_d);
    for (p = bosses)
      translate([p[0], p[1], -0.01])
        cylinder(h = 0.9, d1 = 4.6, d2 = screw_d);
    for (p = [[led1_x, led1_y], [led2_x, led2_y]])
      translate([p[0], p[1], 0.4])
        cylinder(h = lid_t + lip_h, d = led_d);
    for (i = [0 : comb_count - 1])
      translate([-0.2, comb_y0 + i * comb_gap + 0.25, lid_t + 0.3])
        cube([wall + 2, comb_w - 0.5, lip_h]);
    for (x = [8, outer_l - 8 - vhb])
      for (y = [6, outer_w - 6 - vhb])
        translate([x, y, -0.01])
          cube([vhb, vhb, 0.35]);
  }
}

if (PART == "base") padtap_base();
else if (PART == "lid") padtap_lid();
else {
  padtap_base();
  translate([0, 0, base_h + 6]) padtap_lid();
}
