CREATE DATABASE IF NOT EXISTS Kazooha;

DROP TABLE Messages;
CREATE TABLE IF NOT EXISTS Messages (
    id BIGINT NOT NULL PRIMARY KEY,
    guildId BIGINT NOT NULL,
    guildName VARCHAR(100) NOT NULL,
    channelId BIGINT NOT NULL,
    channelName VARCHAR(100) NOT NULL,
    authorId BIGINT NOT NULL,
    authorName VARCHAR(100) NOT NULL,
    sentTime TIMESTAMP NOT NULL,
    content VARCHAR(4000) NOT NULL,
    modified BOOLEAN,
    deleted BOOLEAN
);

CREATE TABLE IF NOT EXISTS Artifacts (
    setId VARCHAR(100) PRIMARY KEY UNIQUE,
    setName VARCHAR(100) NOT NULL UNIQUE,
    flower TEXT NOT NULL,
    plume TEXT NOT NULL,
    sands TEXT NOT NULL,
    goblet TEXT NOT NULL,
    circlet TEXT NOT NULL
);

# pour euh... tester xD
INSERT INTO Artifacts (setId, setName, flower, plume, sands, goblet, circlet) VALUE ('ame_des_profondeurs', 'Âme des profondeurs', '__**Broche plaquée**__
	*Une broche de cape qui a perdu son éclat. Son plaquage en or s''est érodé à cause du vent et des vagues il y a fort longtemps.*

	Une broche dont les couleurs ont flétri sous l''action de la bise et du sel marin.
	Même celui qui parcourt les vagues
	possède quelque souvenir précieux à son cœur.
	De nouveau le vaisseau reprit la mer, et de nouveau le second et le capitaine voguèrent ensemble.
	Pour l''absurde poursuite du capitaine, et pour ses propres souvenirs obscurcis,
	le second entonna son sinistre chant de marin, les baleines et les flots lui servant de chœur :
	« Le flibustier qui renia sa lignée et la sorcière qui le chassait, jamais les quatre mers ne purent aborder... »
	« Et le frère avisé, par la lignée oublié, de la continuité du clan, enfin devint le garant. »
	« Des paroles impossibles à chanter... Ai-je choisi l''illusion, ou la vérité ? »
	« Ayant tout perdu et tout abandonné, dans les vagues amènes j''ai plongé. »
	« Mais peut-être s''agit-il là de la fin la plus indiquée. Hahaha ! »', '__**Brise nostalgique**__
	*Une plume transportée par la brise sifflante et les vagues pourpres de la mer. Le temps a altéré sa forme et sa couleur.*

	La plume rouge volait, menaçante, annonciatrice de la mort à venir.
	Elle échoua un jour aux côtés du corps d''un monstre marin.
	Le second cynique n''était pas originaire de Liyue, mais venait d''un pays gris régi par l''aristocratie.
	On disait de lui qu''il faisait autrefois partie de la noblesse, mais avait été banni de son clan suite à quelque sombre affaire.
	Mais tout ceci n''était que racontars sans fondement. À son arrivée au port, il n''avait sur lui qu''une rapière,
	ainsi qu''une petite plume de couleur saphir, accrochée à sa cape délabrée.
	Plus tard, le vagabond rejoignit le capitaine, et, prenant la mer, les deux affrontèrent vagues gigantesques et monstres marins.
	La plume jusqu''alors d''un bleu pur fut teintée de rouge et se gorgea de sel marin.
	À ses derniers instants,
	il se remémora clairement un passé qu''il avait enfoui sous l''alcool.
	Tel un trésor se révélant sous le sable emporté par les vagues...', '**Boussole en bronze**__
	*Une vieille boussole en bronze. Son aiguille pointe vers un rivage inatteignable, vers un port qui n''existe pas.*

	Une boussole en bronze utilisée par un marin.
	Gardant le cap au milieu des aléas de la vie,
	elle pointe sans faillir dans la direction voulue par le cœur de son détenteur.
	Le capitaine à la mise négligée utilisait autrefois cet outil pour guider son imposant navire,
	triomphant des mers les plus dangereuses et conquérant les tempêtes les plus majestueuses.
	Mais cette boussole guida également celui dont le rire cachait une haine sans limites,
	et qui, en proie au désespoir, appelait la mort et l''alcool à son secours...
	« Vous chantez que le voleur évite la potence à la fin, hein ? »
	« Tant que vous avez une place qui est vôtre quelque part, alors même finir dans le ventre d''un poisson n''est pas si terrible. »
	« N''as-tu pas signé un contrat avec ce navire quand tu as embarqué ? »
	« Le rhum ne t''a quand même pas fait oublier ça, j''espère ?! Hahaha ! »
	« Tant mieux. Parce que l''heure est venue d''honorer ton pacte. »
	« Ainsi donc c''est l''heure ? ... Soit. Plus rien n''a d''importance... »', '__**Calice des profondeurs**__
	*Une coupe ternie qui a été récupérée en mer par hasard. On peut déduire qu''elle a passé du temps dans l''eau d''après son apparence.*

	Une coupe raffinée, aux couleurs quelque peu délavées,
	Polie par le sable des profondeurs sous-marines.
	La coupe exquise glissa de la main du second, faisant naître de minuscules ondes à la surface de l''eau en s''y enfonçant.
	Que vit-elle, perdue au milieu des bancs de poissons, alors que s''estompait la lumière ?
	Et lui, que vit-il dans les ruelles silencieuses du port endormi, aux fenêtres barrées de fleurs de quelque rendez-vous galant ?
	S''enfonçant toujours plus profond, la coupe dorée pénétra dans les songes de la créature marine, et dans les rêves du second...
	« Cette marque humiliante est de ton fait, et un jour, tu paieras. »
	Le clair de lune illumina les yeux de saphir, et la cicatrice à l''aspect si particulier.
	Il la voyait dans ses souvenirs, toujours plus belle, plus froide – et plus fière.
	Mais il réalisa qu''il avait oublié quelles paroles il avait alors prononcées, et en conçut un amer désarroi.
	« Combien de fois ai-je oublié le passé... »
	« Ah ! À quoi bon ressasser les jours d''antan ? »
	« Toute mort est vaine, et aucun salut ne réside dans le passé. »', '__**Calot taché de vin**__
	*Un vieux couvre-chef taché par du vin. Il empeste encore l''alcool aujourd''hui.*

	Ce tricorne dégage une forte odeur d''alcool.
	Sa forme indique le rang de celui qui le porte.
	Le second, dont le penchant pour les tord-boyaux était prononcé, passait ses journées perdu dans une rêverie éthylique, et dessaoulait rarement.
	Puant l''alcool, il restait là à marmonner quelque souvenir obscur.
	Le capitaine jovial ne lui en tenait pas rigueur, lui confiant même d''importantes responsabilités.
	« Après tout, nous n''avons rien à perdre, pas vrai ? Hahaha ! »
	« Le couvre-chef aux relents d''alcool fut projeté dans les airs par la tempête, avant d''être emporté au loin par les flots agités. »
	« Ceux qui sont voués à perdre leur foyer n''ont d''autre choix que de prendre part à des luttes désespérées. »
	« Et ainsi vont-ils, réclamant aux profondeurs les vestiges perdus dans leurs souvenirs. »
	« Le vent et les vagues sont propices. Nous l''avons trouvé. »
	« Le monstre qui hante mes rêves et qui dévore mes nuits... »
	« L''heure de la vengeance a enfin sonné. Hissez les voiles ! »');
