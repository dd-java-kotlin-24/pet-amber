package edu.cnm.deepdive.petamber.server.model.entity

import jakarta.persistence.CascadeType
import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.EnumType
import jakarta.persistence.Enumerated
import jakarta.persistence.FetchType
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import jakarta.persistence.Index
import jakarta.persistence.JoinColumn
import jakarta.persistence.ManyToOne
import jakarta.persistence.OneToMany
import jakarta.persistence.OrderBy
import jakarta.persistence.PrePersist
import jakarta.persistence.Table
import org.hibernate.annotations.CreationTimestamp
import java.util.UUID
import kotlin.time.Instant

@Entity
@Table(
    name = "sighting",
    indexes = [
        Index(columnList = "pet_report_id"),
        Index(columnList = "spotter_id"),
        Index(columnList = "sighting_timestamp"),
        Index(columnList = "latitude, longitude")
    ]
)
class Sighting(

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "pet_report_id", nullable = false, updatable = false)
    var petReport: PetReport,

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "spotter_id", nullable = false, updatable = false)
    var spotter: UserProfile,

    @Column(name = "photo_url", nullable = true, length = 1024)
    var photoUrl: String? = null,

    @Column(name = "sighting_timestamp", nullable = false)
    var sightingTimestamp: Instant,

    @Column(nullable = false)
    var latitude: Double,

    @Column(nullable = false)
    var longitude: Double,

    @Column(name = "location_description", nullable = true, length = 255)
    var locationDescription: String? = null,

    @Enumerated(EnumType.STRING)
    @Column(nullable = true, length = 20)
    var direction: Direction? = null,

    @Column(name = "direction_notes", nullable = true, length = 255)
    var directionNotes: String? = null,

    @Column(nullable = true, columnDefinition = "TEXT")
    var notes: String? = null

) {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "sighting_id", nullable = false, updatable = false)
    var id: Long? = null

    @Column(name = "external_key", nullable = false, updatable = false, unique = true)
    var externalKey: UUID? = null

    @Column(nullable = false, updatable = false)
    @CreationTimestamp
    open var created: Instant? = null

    @OneToMany(
        mappedBy = "sighting",
        fetch = FetchType.LAZY,
        cascade = [CascadeType.ALL],
        orphanRemoval = true
    )
    @OrderBy("created DESC")
    private val _corroborations: MutableList<Corroboration> = mutableListOf()

    val corroborations: List<Corroboration>
        get() = _corroborations.toList()

    @PrePersist
    fun generateFieldValues() {
        if (externalKey == null) {
            externalKey = UUID.randomUUID()
        }
    }

    enum class Direction {
        NORTH,
        NORTHEAST,
        EAST,
        SOUTHEAST,
        SOUTH,
        SOUTHWEST,
        WEST,
        NORTHWEST,
        STATIONARY,
        UNKNOWN
    }

}
