package com.httpurax.certusore;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Re-adds the certus quartz ore blocks that Applied Energistics 2 dropped in 1.19,
 * so you can go mining for certus quartz again instead of hunting meteorites.
 *
 * <p>The four blocks are plain {@link Block}s. Everything else - worldgen, loot tables,
 * ore tags, models and textures - is pure data under {@code src/main/resources/data}
 * and {@code src/main/resources/assets}, which also means the vein frequency can be
 * tuned with a datapack override (see the README).</p>
 */
@Mod(CertusQuartzOre.MOD_ID)
public class CertusQuartzOre {

    public static final String MOD_ID = "certusore";

    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(MOD_ID);
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MOD_ID);

    /** Declared before the blocks so the static initialisers below can fill it. */
    private static final List<DeferredItem<BlockItem>> ORE_ITEMS = new ArrayList<>();

    public static final DeferredBlock<Block> CERTUS_QUARTZ_ORE =
            registerOre("certus_quartz_ore", 3.0F, 3.0F, SoundType.STONE);
    public static final DeferredBlock<Block> DEEPSLATE_CERTUS_QUARTZ_ORE =
            registerOre("deepslate_certus_quartz_ore", 4.5F, 3.0F, SoundType.DEEPSLATE);
    public static final DeferredBlock<Block> CHARGED_CERTUS_QUARTZ_ORE =
            registerOre("charged_certus_quartz_ore", 3.0F, 3.0F, SoundType.STONE);
    public static final DeferredBlock<Block> DEEPSLATE_CHARGED_CERTUS_QUARTZ_ORE =
            registerOre("deepslate_charged_certus_quartz_ore", 4.5F, 3.0F, SoundType.DEEPSLATE);

    public CertusQuartzOre(IEventBus modEventBus) {
        BLOCKS.register(modEventBus);
        ITEMS.register(modEventBus);
        modEventBus.addListener(this::addCreative);
    }

    /**
     * Registers a block plus its BlockItem. Ores need an iron pickaxe to drop anything,
     * matching how AE2's own certus quartz blocks behave.
     */
    private static DeferredBlock<Block> registerOre(String name, float destroyTime, float explosionResistance,
            SoundType sound) {
        DeferredBlock<Block> block = BLOCKS.register(name, () -> new Block(BlockBehaviour.Properties.of()
                .requiresCorrectToolForDrops()
                .strength(destroyTime, explosionResistance)
                .sound(sound)));
        ORE_ITEMS.add(ITEMS.register(name, () -> new BlockItem(block.get(), new Item.Properties())));
        return block;
    }

    private void addCreative(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.NATURAL_BLOCKS) {
            for (DeferredItem<BlockItem> item : ORE_ITEMS) {
                event.accept(item);
            }
        }
    }
}
